"""Image comparison and manipulation utilities."""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Optional, Tuple
from PIL import Image
from skimage.metrics import structural_similarity as ssim


class ImageUtils:
    """Image comparison and manipulation utilities."""
    
    @staticmethod
    def compare_images(
        image1_path: str,
        image2_path: str,
        method: str = 'ssim',
        threshold: float = 0.95
    ) -> Dict:
        """
        Compare two images and return similarity score.
        
        Args:
            image1_path: Path to first image
            image2_path: Path to second image
            method: Comparison method ('ssim', 'mse', 'histogram')
            threshold: Similarity threshold (0.0 - 1.0)
            
        Returns:
            Dictionary with similarity score and match result
        """
        img1 = cv2.imread(image1_path)
        img2 = cv2.imread(image2_path)
        
        if img1 is None:
            raise FileNotFoundError(f"Image not found: {image1_path}")
        if img2 is None:
            raise FileNotFoundError(f"Image not found: {image2_path}")
        
        # Resize images to same dimensions
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        if method == 'ssim':
            score = ImageUtils._compare_ssim(img1, img2)
        elif method == 'mse':
            score = ImageUtils._compare_mse(img1, img2)
        elif method == 'histogram':
            score = ImageUtils._compare_histogram(img1, img2)
        else:
            raise ValueError(f"Invalid comparison method: {method}")
        
        return {
            'similarity': score,
            'threshold': threshold,
            'match': score >= threshold,
            'method': method
        }
    
    @staticmethod
    def _compare_ssim(img1: np.ndarray, img2: np.ndarray) -> float:
        """Compare images using Structural Similarity Index."""
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Calculate SSIM
        score, _ = ssim(gray1, gray2, full=True)
        return float(score)
    
    @staticmethod
    def _compare_mse(img1: np.ndarray, img2: np.ndarray) -> float:
        """Compare images using Mean Squared Error (inverted to similarity)."""
        # Calculate MSE
        mse = np.mean((img1 - img2) ** 2)
        
        # Convert to similarity score (0-1)
        # Lower MSE = higher similarity
        max_mse = 255 ** 2  # Maximum possible MSE for 8-bit images
        similarity = 1 - (mse / max_mse)
        return float(similarity)
    
    @staticmethod
    def _compare_histogram(img1: np.ndarray, img2: np.ndarray) -> float:
        """Compare images using histogram correlation."""
        # Calculate histograms
        hist1 = cv2.calcHist([img1], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([img2], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
        
        # Normalize histograms
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()
        
        # Calculate correlation
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        return float(correlation)
    
    @staticmethod
    def find_image_in_image(
        haystack_path: str,
        needle_path: str,
        confidence: float = 0.8
    ) -> Optional[Dict]:
        """
        Find a smaller image within a larger image.
        
        Args:
            haystack_path: Path to larger image to search in
            needle_path: Path to smaller image to find
            confidence: Matching confidence (0.0 - 1.0)
            
        Returns:
            Dictionary with location and confidence or None if not found
        """
        haystack = cv2.imread(haystack_path)
        needle = cv2.imread(needle_path)
        
        if haystack is None:
            raise FileNotFoundError(f"Image not found: {haystack_path}")
        if needle is None:
            raise FileNotFoundError(f"Image not found: {needle_path}")
        
        # Perform template matching
        result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= confidence:
            needle_h, needle_w = needle.shape[:2]
            return {
                'found': True,
                'confidence': float(max_val),
                'x': max_loc[0] + needle_w // 2,
                'y': max_loc[1] + needle_h // 2,
                'left': max_loc[0],
                'top': max_loc[1],
                'width': needle_w,
                'height': needle_h
            }
        
        return None
    
    @staticmethod
    def get_image_dimensions(image_path: str) -> Tuple[int, int]:
        """
        Get image dimensions.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Tuple of (width, height)
        """
        img = Image.open(image_path)
        return img.size
    
    @staticmethod
    def crop_image(
        image_path: str,
        region: Tuple[int, int, int, int],
        output_path: Optional[str] = None
    ) -> str:
        """
        Crop image to specified region.
        
        Args:
            image_path: Path to image file
            region: Region coordinates (left, top, right, bottom)
            output_path: Output path (auto-generated if not provided)
            
        Returns:
            Path to cropped image
        """
        img = Image.open(image_path)
        cropped = img.crop(region)
        
        if not output_path:
            path = Path(image_path)
            output_path = str(path.parent / f"{path.stem}_cropped{path.suffix}")
        
        cropped.save(output_path)
        return output_path
    
    @staticmethod
    def resize_image(
        image_path: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale: Optional[float] = None,
        output_path: Optional[str] = None
    ) -> str:
        """
        Resize image.
        
        Args:
            image_path: Path to image file
            width: Target width (maintains aspect ratio if height not provided)
            height: Target height (maintains aspect ratio if width not provided)
            scale: Scale factor (e.g., 0.5 for 50%)
            output_path: Output path (auto-generated if not provided)
            
        Returns:
            Path to resized image
        """
        img = Image.open(image_path)
        
        if scale:
            width = int(img.width * scale)
            height = int(img.height * scale)
        elif width and not height:
            height = int(img.height * (width / img.width))
        elif height and not width:
            width = int(img.width * (height / img.height))
        elif not width and not height:
            raise ValueError("Must provide width, height, or scale")
        
        resized = img.resize((width, height), Image.Resampling.LANCZOS)
        
        if not output_path:
            path = Path(image_path)
            output_path = str(path.parent / f"{path.stem}_resized{path.suffix}")
        
        resized.save(output_path)
        return output_path
    
    @staticmethod
    def convert_to_grayscale(
        image_path: str,
        output_path: Optional[str] = None
    ) -> str:
        """
        Convert image to grayscale.
        
        Args:
            image_path: Path to image file
            output_path: Output path (auto-generated if not provided)
            
        Returns:
            Path to grayscale image
        """
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        if not output_path:
            path = Path(image_path)
            output_path = str(path.parent / f"{path.stem}_gray{path.suffix}")
        
        cv2.imwrite(output_path, gray)
        return output_path
    
    @staticmethod
    def highlight_differences(
        image1_path: str,
        image2_path: str,
        output_path: Optional[str] = None,
        color: Tuple[int, int, int] = (0, 0, 255)
    ) -> str:
        """
        Create image highlighting differences between two images.
        
        Args:
            image1_path: Path to first image
            image2_path: Path to second image
            output_path: Output path for diff image
            color: Color for highlighting differences (BGR format)
            
        Returns:
            Path to diff image
        """
        img1 = cv2.imread(image1_path)
        img2 = cv2.imread(image2_path)
        
        # Resize to match dimensions
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Calculate difference
        _, diff = ssim(gray1, gray2, full=True)
        diff = (diff * 255).astype("uint8")
        
        # Threshold the difference
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw rectangles around differences
        result = img1.copy()
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(result, (x, y), (x + w, y + h), color, 2)
        
        if not output_path:
            path = Path(image1_path)
            output_path = str(path.parent / f"{path.stem}_diff{path.suffix}")
        
        cv2.imwrite(output_path, result)
        return output_path
    
    @staticmethod
    def wait_for_image(
        reference_path: str,
        screenshot_func: callable,
        timeout: int = 30,
        interval: int = 1,
        confidence: float = 0.8
    ) -> bool:
        """
        Wait for an image to appear on screen.
        
        Args:
            reference_path: Path to reference image to find
            screenshot_func: Function that takes screenshot and returns path
            timeout: Maximum wait time in seconds
            interval: Check interval in seconds
            confidence: Matching confidence
            
        Returns:
            True if image found within timeout
        """
        import time
        
        elapsed = 0
        while elapsed < timeout:
            screenshot_path = screenshot_func()
            result = ImageUtils.find_image_in_image(screenshot_path, reference_path, confidence)
            
            if result:
                return True
            
            time.sleep(interval)
            elapsed += interval
        
        return False