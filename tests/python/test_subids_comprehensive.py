#!/usr/bin/env python3
"""
Comprehensive test script for Shopee Affiliate API subId formats.
Tests all valid, invalid, and edge case formats.
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add examples directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../examples/python'))
from shopee_affiliate_client import ShopeeAffiliateClient

class SubIdTester:
    """Test various subId formats against Shopee Affiliate API."""

    def __init__(self):
        self.app_id = os.getenv("SHOPEE_APP_ID")
        self.app_secret = os.getenv("SHOPEE_APP_SECRET")

        if not self.app_id or not self.app_secret:
            raise ValueError("SHOPEE_APP_ID and SHOPEE_APP_SECRET must be set in environment variables")

        self.client = ShopeeAffiliateClient(self.app_id, self.app_secret)
        self.results = []

    def test_subid_format(self, sub_ids: List[str], test_name: str, expected: str = "unknown") -> Dict[str, Any]:
        """
        Test a specific subId format.

        Args:
            sub_ids: List of subId values to test
            test_name: Descriptive name for the test
            expected: Expected result ('valid', 'invalid', or 'unknown')

        Returns:
            Dictionary with test results
        """
        print(f"\n{'='*60}")
        print(f"Test: {test_name}")
        print(f"Format: {json.dumps(sub_ids)}")
        print(f"Expected: {expected}")

        # Use a test URL for short link generation
        test_url = "https://shopee.com.br/product-test-12345"

        result = {
            "test_name": test_name,
            "format": sub_ids,
            "expected": expected,
            "timestamp": datetime.now().isoformat()
        }

        try:
            # Make API request using generateShortLink mutation
            response = self.client.generate_short_link(
                origin_url=test_url,
                sub_ids=sub_ids
            )

            result["response"] = json.dumps(response, ensure_ascii=False)[:500]  # Limit response size

            if "errors" in response:
                result["result"] = "ERROR"
                result["error"] = response["errors"][0].get("message", "Unknown error")
                print(f"✗ Result: ERROR")
                print(f"  Error: {result['error']}")
            else:
                result["result"] = "SUCCESS"
                result["error"] = None
                short_link = response.get("data", {}).get("generateShortLink", {}).get("shortLink", "")
                print(f"✓ Result: SUCCESS")
                if short_link:
                    print(f"  ShortLink: {short_link}")

        except Exception as e:
            result["result"] = "EXCEPTION"
            result["error"] = str(e)
            print(f"✗ Result: EXCEPTION")
            print(f"  Error: {str(e)}")

        self.results.append(result)
        return result

    def run_all_tests(self):
        """Run all comprehensive tests."""
        print("\n" + "="*60)
        print("SHOPEE AFFILIATE API - COMPREHENSIVE SUBID FORMAT TESTS")
        print("="*60)
        print(f"Started at: {datetime.now().isoformat()}")

        # VALID FORMATS (Expected to work)
        print("\n" + "="*60)
        print("CATEGORY 1: VALID FORMATS")
        print("="*60)

        self.test_subid_format([], "Empty array", "valid")
        self.test_subid_format(["s1", "s2", "s3", "s4", "s5"], "Simple letters with numbers", "valid")
        self.test_subid_format(["a", "b", "c", "d", "e"], "Single letters", "valid")
        self.test_subid_format(["1", "2", "3", "4", "5"], "Numbers as strings", "valid")
        self.test_subid_format(["promo", "sale", "topo"], "Short words", "valid")
        self.test_subid_format(["promo1", "promo2", "sale1"], "Words with numbers", "valid")
        self.test_subid_format(["email"], "Single word: email", "valid")
        self.test_subid_format(["canal"], "Single word: canal", "valid")
        self.test_subid_format(["s1", "email", "2"], "Mixed format", "valid")
        self.test_subid_format(["abc"], "Single 3-letter word", "valid")
        self.test_subid_format(["teste123"], "Word ending with numbers", "valid")
        self.test_subid_format(["xyz123abc"], "Alphanumeric mix", "valid")

        # INVALID FORMATS (Expected to fail)
        print("\n" + "="*60)
        print("CATEGORY 2: INVALID FORMATS")
        print("="*60)

        self.test_subid_format(["_test"], "Underscore at start", "invalid")
        self.test_subid_format(["sub_id"], "Underscore in middle", "invalid")
        self.test_subid_format(["sub_1", "test_2"], "Underscore with numbers", "invalid")
        self.test_subid_format(["test-1"], "Hyphen", "invalid")
        self.test_subid_format(["promo-2024"], "Hyphen with numbers", "invalid")
        self.test_subid_format(["test.1"], "Dot separator", "invalid")
        self.test_subid_format(["v2.0"], "Version with dot", "invalid")
        self.test_subid_format(["test@1"], "At symbol", "invalid")
        self.test_subid_format(["promo#2024"], "Hash symbol", "invalid")
        self.test_subid_format(["utm_source"], "UTM prefix (reserved)", "invalid")
        self.test_subid_format(["utm_medium"], "UTM prefix (reserved)", "invalid")
        self.test_subid_format(["subId"], "CamelCase", "invalid")
        self.test_subid_format(["testId"], "CamelCase mixed", "invalid")
        self.test_subid_format(["test!", "promo?"], "Special characters", "invalid")
        self.test_subid_format(["test space"], "Space in name", "invalid")

        # EDGE CASES
        print("\n" + "="*60)
        print("CATEGORY 3: EDGE CASES")
        print("="*60)

        self.test_subid_format(["s1", "s2", "s3", "s4", "s5", "s6"], "Array with 6 items (limit is 5)", "invalid")
        self.test_subid_format(["a" * 100], "Very long string (100 chars)", "unknown")
        self.test_subid_format(["a" * 50], "Long string (50 chars)", "unknown")
        self.test_subid_format(["café"], "Unicode with accent", "unknown")
        self.test_subid_format(["promoção"], "Unicode with special char", "unknown")
        self.test_subid_format(["janeiro"], "Month name: January", "valid")
        self.test_subid_format(["fevereiro"], "Month name: February", "valid")
        self.test_subid_format(["123"], "Pure numeric string", "valid")
        self.test_subid_format(["0"], "Zero as string", "valid")
        self.test_subid_format(["test1test2test3test4test5"], "Long concatenated word", "unknown")
        self.test_subid_format(["UPPERCASE"], "All uppercase", "unknown")
        self.test_subid_format(["MixedCase"], "Mixed case (no numbers)", "unknown")
        self.test_subid_format([""], "Empty string", "invalid")

        # Additional tests for specific patterns
        print("\n" + "="*60)
        print("CATEGORY 4: ADDITIONAL PATTERNS")
        print("="*60)

        self.test_subid_format(["test123456"], "Many trailing numbers", "valid")
        self.test_subid_format(["123test"], "Leading numbers", "unknown")
        self.test_subid_format(["abc123xyz"], "Numbers in middle", "valid")
        self.test_subid_format(["a1b2c3"], "Alternating letters and numbers", "valid")
        self.test_subid_format(["promo"], "Lowercase only", "valid")
        self.test_subid_format(["PROMO"], "Uppercase only", "unknown")
        self.test_subid_format(["s1", "s2", "s3"], "3 items", "valid")
        self.test_subid_format(["s1", "s2", "s3", "s4"], "4 items", "valid")
        self.test_subid_format(["s1", "s2", "s3", "s4", "s5"], "5 items (max)", "valid")

    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)

        total = len(self.results)
        success = sum(1 for r in self.results if r["result"] == "SUCCESS")
        error = sum(1 for r in self.results if r["result"] == "ERROR")
        exception = sum(1 for r in self.results if r["result"] == "EXCEPTION")

        print(f"\nTotal tests: {total}")
        print(f"  SUCCESS: {success}")
        print(f"  ERROR: {error}")
        print(f"  EXCEPTION: {exception}")

        # Categorize by expected results
        print("\n" + "-"*60)
        print("VALID FORMAT TESTS:")
        valid_tests = [r for r in self.results if r["expected"] == "valid"]
        for test in valid_tests:
            status = "✓" if test["result"] == "SUCCESS" else "✗"
            print(f"  {status} {test['test_name']}: {test['result']}")

        print("\n" + "-"*60)
        print("INVALID FORMAT TESTS:")
        invalid_tests = [r for r in self.results if r["expected"] == "invalid"]
        for test in invalid_tests:
            status = "✓" if test["result"] == "ERROR" else "✗"
            print(f"  {status} {test['test_name']}: {test['result']}")

        print("\n" + "-"*60)
        print("UNKNOWN EXPECTATION TESTS:")
        unknown_tests = [r for r in self.results if r["expected"] == "unknown"]
        for test in unknown_tests:
            print(f"  • {test['test_name']}: {test['result']}")

        # Save results to file
        results_file = "/Users/gabrielramos/shopee_afiliados_docs/tests/python/subid_test_results.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_tests": total,
                "success": success,
                "error": error,
                "exception": exception,
                "results": self.results
            }, f, indent=2, ensure_ascii=False)

        print(f"\nDetailed results saved to: {results_file}")
        print(f"Test completed at: {datetime.now().isoformat()}")
        print("="*60)

def main():
    """Main entry point."""
    try:
        tester = SubIdTester()
        tester.run_all_tests()
        tester.print_summary()
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
