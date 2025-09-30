"""OCR (Optical Character Recognition) utility functions."""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image
import pytesseract
import cv2
import numpy as np


class OCRUtils:
    """OCR utilities for text extraction from images."""
    
    def __init__(
        self,
        tesseract_cmd: Optional[str] = None,
        language: str = 'eng',
        config: str = '--psm 6'
    ):
        """
        Initialize OCR utilities.
        
        Args:
            tesseract_cmd: Path to tesseract executable
            language: OCR language (default: 'eng')
            config: Tesseract configuration string
        """
        self.language = language
        self.config = config
        
        # Set tesseract command path if provided
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        elif os.name == 'nt':  # Windows
            # Try common Windows installation paths
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
    
    def extract_text(
        self,
        image_path: str,
        preprocess: bool = True,
        confidence_threshold: int = 0
    ) -> str:
        """
        Extract text from image.
        
        Args:
            image_path: Path to image file
            preprocess: Apply image preprocessing
            confidence_threshold: Minimum confidence (0-100)
            
        Returns:
            Extracted text
        """
        image = self._load_image(image_path)
        
        if preprocess:
            image = self._preprocess_image(image)
        
        # Extract text
        text = pytesseract.image_to_string(
            image,
            lang=self.language,
            config=self.config
        )
        
        # Filter by confidence if threshold is set
        if confidence_threshold > 0:
            data = self.extract_text_with_details(image_path, preprocess)
            filtered_text = []
            for item in data:
                if item['confidence'] >= confidence_threshold:
                    filtered_text.append(item['text'])
            return ' '.join(filtered_text)
        
        return text.strip()
    
    def extract_text_with_details(
        self,
        image_path: str,
        preprocess: bool = True
    ) -> List[Dict]:
        """
        Extract text with position and confidence details.
        
        Args:
            image_path: Path to image file
            preprocess: Apply image preprocessing
            
        Returns:
            List of dictionaries with text, position, and confidence
        """
        image = self._load_image(image_path)
        
        if preprocess:
            image = self._preprocess_image(image)
        
        # Get detailed data
        data = pytesseract.image_to_data(
            image,
            lang=self.language,
            config=self.config,
            output_type=pytesseract.Output.DICT
        )
        
        results = []
        n_boxes = len(data['text'])
        
        for i in range(n_boxes):
            if int(data['conf'][i]) > 0:
                results.append({
                    'text': data['text'][i],
                    'confidence': int(data['conf'][i]),
                    'left': data['left'][i],
                    'top': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i],
                    'block_num': data['block_num'][i],
                    'line_num': data['line_num'][i],
                    'word_num': data['word_num'][i]
                })
        
        return results
    
    def extract_text_from_region(
        self,
        image_path: str,
        region: Tuple[int, int, int, int],
        preprocess: bool = True
    ) -> str:
        """
        Extract text from specific region of image.
        
        Args:
            image_path: Path to image file
            region: Region coordinates (left, top, right, bottom)
            preprocess: Apply image preprocessing
            
        Returns:
            Extracted text from region
        """
        image = Image.open(image_path)
        cropped = image.crop(region)
        
        # Save to temporary file
        temp_path = Path(image_path).parent / 'temp_crop.png'
        cropped.save(temp_path)
        
        try:
            text = self.extract_text(str(temp_path), preprocess)
        finally:
            if temp_path.exists():
                temp_path.unlink()
        
        return text
    
    def find_text_location(
        self,
        image_path: str,
        search_text: str,
        preprocess: bool = True
    ) -> Optional[Dict]:
        """
        Find location of specific text in image.
        
        Args:
            image_path: Path to image file
            search_text: Text to search for
            preprocess: Apply image preprocessing
            
        Returns:
            Dictionary with text location or None if not found
        """
        details = self.extract_text_with_details(image_path, preprocess)
        
        for item in details:
            if search_text.lower() in item['text'].lower():
                return {
                    'text': item['text'],
                    'x': item['left'] + item['width'] // 2,
                    'y': item['top'] + item['height'] // 2,
                    'left': item['left'],
                    'top': item['top'],
                    'width': item['width'],
                    'height': item['height'],
                    'confidence': item['confidence']
                }
        
        return None
    
    def verify_text_present(
        self,
        image_path: str,
        expected_text: str,
        case_sensitive: bool = False,
        preprocess: bool = True
    ) -> bool:
        """
        Verify if text is present in image.
        
        Args:
            image_path: Path to image file
            expected_text: Text to verify
            case_sensitive: Case-sensitive comparison
            preprocess: Apply image preprocessing
            
        Returns:
            True if text is found
        """
        extracted_text = self.extract_text(image_path, preprocess)
        
        if not case_sensitive:
            extracted_text = extracted_text.lower()
            expected_text = expected_text.lower()
        
        return expected_text in extracted_text
    
    def compare_text(
        self,
        image_path: str,
        expected_text: str,
        exact_match: bool = False,
        preprocess: bool = True
    ) -> bool:
        """
        Compare extracted text with expected text.
        
        Args:
            image_path: Path to image file
            expected_text: Expected text
            exact_match: Require exact match (ignores whitespace by default)
            preprocess: Apply image preprocessing
            
        Returns:
            True if text matches
        """
        extracted_text = self.extract_text(image_path, preprocess)
        
        if exact_match:
            return extracted_text == expected_text
        else:
            # Normalize whitespace
            extracted_normalized = ' '.join(extracted_text.split())
            expected_normalized = ' '.join(expected_text.split())
            return extracted_normalized == expected_normalized
    
    def _load_image(self, image_path: str) -> Image.Image:
        """Load image from file."""
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        return Image.open(image_path)
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results.
        
        Args:
            image: PIL Image
            
        Returns:
            Preprocessed image
        """
        # Convert PIL Image to OpenCV format
        img_array = np.array(image)
        
        # Convert to grayscale if not already
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh)
        
        # Convert back to PIL Image
        return Image.fromarray(denoised)
    
    def extract_numbers(
        self,
        image_path: str,
        preprocess: bool = True
    ) -> List[str]:
        """
        Extract only numbers from image.
        
        Args:
            image_path: Path to image file
            preprocess: Apply image preprocessing
            
        Returns:
            List of extracted numbers
        """
        # Use digits-only config
        config = self.config + ' -c tessedit_char_whitelist=0123456789'
        image = self._load_image(image_path)
        
        if preprocess:
            image = self._preprocess_image(image)
        
        text = pytesseract.image_to_string(image, lang=self.language, config=config)
        
        # Extract numbers
        import re
        numbers = re.findall(r'\d+', text)
        return numbers