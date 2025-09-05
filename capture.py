#!/usr/bin/env python3
"""
Forensic Capture Tool
Advanced web data capture and analysis tool for forensic investigations
"""

import asyncio
import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import hashlib
import uuid

from playwright.async_api import async_playwright, Browser, Page
import aiohttp
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests


class ForensicCapture:
    """
    Advanced forensic capture tool for web data collection and analysis
    """
    
    def __init__(self, labels: List[str], output_dir: str, min_bytes: int = 1000000):
        self.labels = labels
        self.output_dir = Path(output_dir)
        self.min_bytes = min_bytes
        self.session_id = str(uuid.uuid4())
        self.capture_metadata = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'labels': labels,
            'min_bytes': min_bytes,
            'captures': []
        }
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for organized storage
        (self.output_dir / 'screenshots').mkdir(exist_ok=True)
        (self.output_dir / 'html_dumps').mkdir(exist_ok=True)
        (self.output_dir / 'network_logs').mkdir(exist_ok=True)
        (self.output_dir / 'metadata').mkdir(exist_ok=True)
        
        print(f"[INFO] Forensic Capture initialized")
        print(f"[INFO] Session ID: {self.session_id}")
        print(f"[INFO] Output directory: {self.output_dir}")
        print(f"[INFO] Target labels: {', '.join(labels)}")
        print(f"[INFO] Minimum capture size: {min_bytes} bytes")

    async def setup_browser(self) -> Browser:
        """Setup browser with forensic-grade settings"""
        self.playwright = await async_playwright().start()
        browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--single-process',
                '--disable-gpu',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding'
            ]
        )
        return browser

    async def capture_page_data(self, page: Page, url: str, label: str) -> Dict[str, Any]:
        """Comprehensive page data capture"""
        capture_timestamp = datetime.now().isoformat()
        capture_id = hashlib.md5(f"{url}_{label}_{capture_timestamp}".encode()).hexdigest()
        
        print(f"[INFO] Capturing data for {label} from {url}")
        
        # Navigate to page
        try:
            response = await page.goto(url, wait_until='load', timeout=30000)
            if not response or not response.ok:
                print(f"[WARNING] Failed to load {url} - HTTP {response.status if response else 'No response'}")
                return None
        except Exception as e:
            print(f"[ERROR] Navigation failed for {url}: {str(e)}")
            return None

        # Wait for page to fully load
        try:
            await page.wait_for_load_state('networkidle', timeout=10000)
        except Exception:
            # If networkidle times out, continue anyway
            print(f"[WARNING] Network idle timeout for {url}, continuing...")
        
        await page.wait_for_timeout(1000)  # Brief wait for dynamic content

        # Capture HTML content
        html_content = await page.content()
        html_size = len(html_content.encode('utf-8'))
        
        if html_size < self.min_bytes:
            print(f"[WARNING] HTML content too small ({html_size} bytes < {self.min_bytes}), skipping {url}")
            return None

        # Save HTML dump
        html_file = self.output_dir / 'html_dumps' / f"{capture_id}_{label}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Capture screenshot
        screenshot_file = self.output_dir / 'screenshots' / f"{capture_id}_{label}.png"
        await page.screenshot(path=str(screenshot_file), full_page=True)

        # Extract metadata from page
        title = await page.title()
        url_final = page.url
        
        # Extract text content
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text(strip=True)
        
        # Capture network requests (simplified)
        network_file = self.output_dir / 'network_logs' / f"{capture_id}_{label}_network.json"
        
        # Basic page analysis
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        images = [img.get('src') for img in soup.find_all('img', src=True)]
        forms = len(soup.find_all('form'))
        
        capture_data = {
            'capture_id': capture_id,
            'label': label,
            'url_original': url,
            'url_final': url_final,
            'timestamp': capture_timestamp,
            'title': title,
            'html_size': html_size,
            'text_length': len(text_content),
            'links_count': len(links),
            'images_count': len(images),
            'forms_count': forms,
            'files': {
                'html': str(html_file.relative_to(self.output_dir)),
                'screenshot': str(screenshot_file.relative_to(self.output_dir)),
                'network': str(network_file.relative_to(self.output_dir))
            },
            'hash_md5': hashlib.md5(html_content.encode('utf-8')).hexdigest(),
            'hash_sha256': hashlib.sha256(html_content.encode('utf-8')).hexdigest()
        }
        
        # Save network data (placeholder for now)
        network_data = {
            'capture_id': capture_id,
            'timestamp': capture_timestamp,
            'requests': []  # Would be populated with actual network monitoring
        }
        
        with open(network_file, 'w') as f:
            json.dump(network_data, f, indent=2)
        
        print(f"[SUCCESS] Captured {label}: {html_size} bytes from {url_final}")
        return capture_data

    async def search_and_capture(self, label: str) -> List[Dict[str, Any]]:
        """Search for targets and capture data"""
        # Simulated search URLs - in real forensic work, these would be actual target URLs
        target_urls = [
            f"https://httpbin.org/html",  # Test endpoint with HTML
            f"https://httpbin.org/json",  # Test endpoint
            f"https://www.wikipedia.org/",  # Reliable test site
        ]
        
        captures = []
        
        for url in target_urls:
            browser = None
            page = None
            try:
                browser = await self.setup_browser()
                page = await browser.new_page()
                
                # Set up request interception for forensic logging
                async def handle_request(request):
                    print(f"[NETWORK] {request.method} {request.url}")
                
                page.on("request", handle_request)
                
                capture_data = await self.capture_page_data(page, url, label)
                if capture_data:
                    captures.append(capture_data)
                    self.capture_metadata['captures'].append(capture_data)
                
                await page.wait_for_timeout(1000)  # Rate limiting
                    
            except Exception as e:
                print(f"[ERROR] Capture failed for {url}: {str(e)}")
            
            finally:
                if page:
                    try:
                        await page.close()
                    except Exception:
                        pass
                if browser:
                    try:
                        await browser.close()
                    except Exception:
                        pass
                if hasattr(self, 'playwright'):
                    try:
                        await self.playwright.stop()
                    except Exception:
                        pass
        
        return captures

    async def run_capture(self):
        """Execute the forensic capture process"""
        print(f"\n[INFO] Starting forensic capture process...")
        print(f"[INFO] Processing {len(self.labels)} labels: {', '.join(self.labels)}")
        
        all_captures = []
        
        # Process each label
        with tqdm(total=len(self.labels), desc="Processing labels") as pbar:
            for label in self.labels:
                print(f"\n[INFO] Processing label: {label}")
                captures = await self.search_and_capture(label)
                all_captures.extend(captures)
                pbar.update(1)
                
                # Brief pause between labels
                await asyncio.sleep(1)
        
        # Save final metadata
        self.capture_metadata['total_captures'] = len(all_captures)
        self.capture_metadata['completion_timestamp'] = datetime.now().isoformat()
        
        metadata_file = self.output_dir / 'metadata' / f"session_{self.session_id}.json"
        with open(metadata_file, 'w') as f:
            json.dump(self.capture_metadata, f, indent=2)
        
        # Generate summary report
        await self.generate_report()
        
        print(f"\n[SUCCESS] Forensic capture completed!")
        print(f"[INFO] Total captures: {len(all_captures)}")
        print(f"[INFO] Session metadata: {metadata_file}")
        print(f"[INFO] Output directory: {self.output_dir}")

    async def generate_report(self):
        """Generate forensic analysis report"""
        report_file = self.output_dir / f"forensic_report_{self.session_id}.txt"
        
        with open(report_file, 'w') as f:
            f.write("FORENSIC CAPTURE REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Timestamp: {self.capture_metadata['timestamp']}\n")
            f.write(f"Labels: {', '.join(self.labels)}\n")
            f.write(f"Minimum bytes threshold: {self.min_bytes}\n")
            f.write(f"Total captures: {len(self.capture_metadata['captures'])}\n\n")
            
            f.write("CAPTURE DETAILS:\n")
            f.write("-" * 30 + "\n")
            
            for capture in self.capture_metadata['captures']:
                f.write(f"\nLabel: {capture['label']}\n")
                f.write(f"URL: {capture['url_final']}\n")
                f.write(f"Title: {capture['title']}\n")
                f.write(f"Size: {capture['html_size']} bytes\n")
                f.write(f"MD5: {capture['hash_md5']}\n")
                f.write(f"SHA256: {capture['hash_sha256']}\n")
                f.write(f"Files: {capture['files']}\n")
        
        print(f"[INFO] Report generated: {report_file}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Forensic Web Capture Tool")
    parser.add_argument('--labels', nargs='+', required=True,
                      help='Target labels for capture (e.g., RHO-TECH PIPETECH)')
    parser.add_argument('--out', required=True,
                      help='Output directory for captured data')
    parser.add_argument('--min-bytes', type=int, default=1000000,
                      help='Minimum bytes threshold for captures')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        print("[DEBUG] Verbose mode enabled")
        print(f"[DEBUG] Arguments: {args}")
    
    # Initialize forensic capture tool
    forensic_tool = ForensicCapture(
        labels=args.labels,
        output_dir=args.out,
        min_bytes=args.min_bytes
    )
    
    # Run the capture process
    try:
        asyncio.run(forensic_tool.run_capture())
    except KeyboardInterrupt:
        print("\n[INFO] Capture interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Capture failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()