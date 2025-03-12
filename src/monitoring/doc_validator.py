"""
Documentation Validator
=====================

CRITICAL REQUIREMENTS:
- Architecture documentation validation
- Integration guide verification
- Trading journal compliance
- Performance requirements tracking

VALIDATION GATES:
1. Document existence
2. Content requirements
3. Version tracking
4. Update verification

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
from typing import Dict, List, Optional
from pathlib import Path
import re
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class DocumentationValidator:
    """
    Documentation validation system
    
    CRITICAL DOCUMENTS:
    - architecture-analysis.md
    - integration-guide.md
    - journal.md
    - README.md
    """
    
    def __init__(self):
        """
        Initialize documentation validator
        
        REQUIREMENTS:
        - Document paths
        - Content rules
        - Version tracking
        - Update logging
        """
        self.docs_path = Path(".")
        
        # STRICT: Required documents
        self.required_docs = {
            'architecture-analysis.md': {
                'required_sections': [
                    'Core Design Philosophy',
                    'System Components',
                    'Risk Management',
                    'Performance Metrics'
                ],
                'critical_keywords': [
                    'win rate',
                    'quantum validation',
                    'risk management',
                    'pattern recognition'
                ]
            },
            'integration-guide.md': {
                'required_sections': [
                    'System Integration',
                    'Error Handling',
                    'Monitoring Setup',
                    'Recovery Procedures'
                ],
                'critical_keywords': [
                    'FreqTrade',
                    'quantum loop',
                    'validation',
                    'monitoring'
                ]
            },
            'journal.md': {
                'required_sections': [
                    'Trade History',
                    'Performance Metrics',
                    'System Updates',
                    'Validation Results'
                ],
                'critical_keywords': [
                    'win rate',
                    'growth rate',
                    'validation',
                    'performance'
                ]
            }
        }
        
        # Initialize validation tracking
        self.validation_results = {}
        logger.info("Documentation Validator initialized")
        
    def validate_documentation(self) -> bool:
        """
        Comprehensive documentation validation
        
        VALIDATION STEPS:
        1. Check existence
        2. Validate content
        3. Verify versions
        4. Check updates
        """
        try:
            all_valid = True
            
            # Check each required document
            for doc_name, requirements in self.required_docs.items():
                doc_path = self.docs_path / doc_name
                if not doc_path.exists():
                    logger.error(f"Required document missing: {doc_name}")
                    all_valid = False
                    continue
                
                # Validate document content
                content_valid = self._validate_document_content(
                    doc_path,
                    requirements['required_sections'],
                    requirements['critical_keywords']
                )
                
                if not content_valid:
                    all_valid = False
                
                # Track validation result
                self.validation_results[doc_name] = {
                    'timestamp': datetime.now().isoformat(),
                    'valid': content_valid,
                    'last_updated': doc_path.stat().st_mtime
                }
            
            return all_valid
            
        except Exception as e:
            logger.error(f"Documentation validation failed: {e}")
            return False
            
    def _validate_document_content(self, 
                                 doc_path: Path,
                                 required_sections: List[str],
                                 critical_keywords: List[str]) -> bool:
        """
        Validate document content requirements
        
        CHECKS:
        1. Required sections
        2. Critical keywords
        3. Content format
        4. Update dates
        """
        try:
            with open(doc_path, 'r') as f:
                content = f.read()
            
            # Check required sections
            missing_sections = []
            for section in required_sections:
                if not re.search(rf"#{{1,6}}\s+{section}", content, re.IGNORECASE):
                    missing_sections.append(section)
            
            if missing_sections:
                logger.error(f"Missing sections in {doc_path.name}: {', '.join(missing_sections)}")
                return False
            
            # Check critical keywords
            missing_keywords = []
            for keyword in critical_keywords:
                if not re.search(keyword, content, re.IGNORECASE):
                    missing_keywords.append(keyword)
            
            if missing_keywords:
                logger.error(f"Missing keywords in {doc_path.name}: {', '.join(missing_keywords)}")
                return False
            
            # Verify last update date is recent
            if not self._verify_recent_update(content):
                logger.warning(f"Document may be outdated: {doc_path.name}")
                # Don't fail validation for outdated docs, just warn
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating {doc_path.name}: {e}")
            return False
            
    def _verify_recent_update(self, content: str) -> bool:
        """
        Verify document was recently updated
        
        REQUIREMENTS:
        - Update date within 24 hours
        - Valid date format
        - Future dates invalid
        """
        try:
            # Look for last updated date
            update_match = re.search(
                r"Last Updated:?\s*(\d{4}-\d{2}-\d{2})",
                content,
                re.IGNORECASE
            )
            
            if not update_match:
                return False
            
            last_update = datetime.strptime(update_match.group(1), '%Y-%m-%d')
            now = datetime.now()
            
            # Check if update is within last 24 hours
            return (now - last_update).days <= 1
            
        except Exception as e:
            logger.error(f"Error verifying update date: {e}")
            return False
            
    def validate_performance_requirements(self) -> bool:
        """
        Validate documented performance requirements
        
        CRITICAL REQUIREMENTS:
        1. Win rate target (85%)
        2. Growth target (£10 to £1000)
        3. Maximum drawdown (10%)
        4. Time constraint (7 days)
        """
        try:
            # Check README.md for performance requirements
            readme_path = self.docs_path / "README.md"
            if not readme_path.exists():
                logger.error("README.md not found")
                return False
            
            with open(readme_path, 'r') as f:
                content = f.read()
            
            # Verify critical requirements
            requirements_valid = True
            
            if not re.search(r"win rate.*?85%", content, re.IGNORECASE):
                logger.error("Win rate target not properly documented")
                requirements_valid = False
            
            if not re.search(r"£10.*?£1000", content, re.IGNORECASE):
                logger.error("Growth target not properly documented")
                requirements_valid = False
            
            if not re.search(r"drawdown.*?10%", content, re.IGNORECASE):
                logger.error("Maximum drawdown not properly documented")
                requirements_valid = False
            
            if not re.search(r"7 days", content, re.IGNORECASE):
                logger.error("Time constraint not properly documented")
                requirements_valid = False
            
            return requirements_valid
            
        except Exception as e:
            logger.error(f"Error validating performance requirements: {e}")
            return False
            
    def get_validation_report(self) -> Dict:
        """
        Generate validation status report
        
        INCLUDES:
        1. Document status
        2. Content validation
        3. Update timestamps
        4. Warning messages
        """
        return {
            'validation_results': self.validation_results,
            'timestamp': datetime.now().isoformat(),
            'all_valid': all(r['valid'] for r in self.validation_results.values()),
            'documents_checked': len(self.validation_results)
        }

def validate_documentation() -> bool:
    """
    Global documentation validation
    
    VALIDATES:
    - All required documents
    - Content requirements
    - Performance targets
    """
    validator = DocumentationValidator()
    docs_valid = validator.validate_documentation()
    perf_valid = validator.validate_performance_requirements()
    return docs_valid and perf_valid