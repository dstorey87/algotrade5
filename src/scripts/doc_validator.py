import json
import os
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class DocumentValidator:
    def __init__(self):
        self.config_path = Path("config/.agent_config.json")
        self.cache_path = Path("config/.doc_cache.json")
        self.config = self._load_config()
        self.architecture_doc = Path(self.config["critical_docs"]["architecture"])
        self.integration_doc = Path(self.config["critical_docs"]["integration"])
        self.doc_content = {}
        self.sections_to_monitor = self.config["doc_sections_to_monitor"]
        self.cache = self._load_cache()
        self.cache_valid_hours = 1  # Cache validity period

    def _load_config(self) -> Dict:
        """Load agent configuration"""
        if not self.config_path.exists():
            raise FileNotFoundError("Agent configuration not found")
        with open(self.config_path) as f:
            return json.load(f)

    def _load_cache(self) -> Dict:
        """Load document cache"""
        if self.cache_path.exists():
            try:
                with open(self.cache_path) as f:
                    return json.load(f)
            except:
                return {"last_update": None, "hashes": {}, "content": {}}
        return {"last_update": None, "hashes": {}, "content": {}}

    def _save_cache(self):
        """Save document cache"""
        os.makedirs(self.cache_path.parent, exist_ok=True)
        with open(self.cache_path, 'w') as f:
            json.dump(self.cache, f)

    def _get_file_hash(self, path: Path) -> str:
        """Get SHA256 hash of file contents"""
        if not path.exists():
            return ""
        with open(path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid"""
        if not self.cache["last_update"]:
            return False
        
        last_update = datetime.fromisoformat(self.cache["last_update"])
        if datetime.now() - last_update > timedelta(hours=self.cache_valid_hours):
            return False

        # Check if files have changed
        for doc_name, doc_path in [
            ("architecture", self.architecture_doc),
            ("integration", self.integration_doc)
        ]:
            current_hash = self._get_file_hash(doc_path)
            if current_hash != self.cache["hashes"].get(doc_name, ""):
                return False

        return True

    def _read_doc(self, doc_path: Path) -> str:
        """Read document content with caching"""
        if not doc_path.exists():
            raise FileNotFoundError(f"Critical document not found: {doc_path}")
        with open(doc_path) as f:
            return f.read()

    def validate_docs(self) -> bool:
        """Validate documentation with caching"""
        try:
            # Check if cache is valid
            if self._is_cache_valid():
                self.doc_content = self.cache["content"]
                return True

            # Read and validate documents
            self.doc_content = {
                "architecture": self._read_doc(self.architecture_doc),
                "integration": self._read_doc(self.integration_doc)
            }

            # Verify all required sections exist
            for section in self.sections_to_monitor:
                if not any(section in doc for doc in self.doc_content.values()):
                    raise ValueError(f"Required section '{section}' not found in documentation")

            # Validate against architectural requirements
            arch_reqs = self.config["architecture_requirements"]
            if not all(
                str(req) in self.doc_content["architecture"] 
                for req in [
                    arch_reqs["target_success_rate"],
                    arch_reqs["risk_parameters"]["max_position_size"],
                    arch_reqs["risk_parameters"]["position_scaling"]
                ]
            ):
                raise ValueError("Documentation missing critical architectural requirements")

            # Update cache
            self.cache.update({
                "last_update": datetime.now().isoformat(),
                "hashes": {
                    "architecture": self._get_file_hash(self.architecture_doc),
                    "integration": self._get_file_hash(self.integration_doc)
                },
                "content": self.doc_content
            })
            self._save_cache()

            return True

        except Exception as e:
            print(f"Documentation validation failed: {str(e)}")
            return False

    def get_doc_content(self) -> Dict[str, str]:
        """Return cached document content"""
        if not self.doc_content and self._is_cache_valid():
            self.doc_content = self.cache["content"]
        return self.doc_content

    def invalidate_cache(self):
        """Force cache invalidation"""
        self.cache = {"last_update": None, "hashes": {}, "content": {}}
        self._save_cache()

# Make the validator available globally
_validator = DocumentValidator()

def validate_documentation() -> bool:
    """Global function to validate documentation"""
    return _validator.validate_docs()

def get_documentation() -> Dict[str, str]:
    """Global function to get documentation content"""
    return _validator.get_doc_content()

def invalidate_doc_cache():
    """Global function to invalidate document cache"""
    _validator.invalidate_cache()