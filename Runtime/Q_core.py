from pathlib import Path
import subprocess
import re

class QObject:
    def __init__(self, path):
        self.path = path
        self.ext = Path(path).suffix
        self.language = None
        self.type = None


class QDetector:
    MAP = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".rs": "rust",
        ".go": "golang",
        ".sol": "solidity",
        ".md": "markdown",
        ".json": "data",
    }

    def detect(self, path):
        obj = QObject(path)
        obj.language = self.MAP.get(obj.ext, "unknown")
        obj.type = "source" if obj.language != "unknown" else "unknown"
        return obj


class QAnalyzer:
    def analyze(self, obj: QObject):
        if obj.language == "python":
            return self._py(obj.path)
        if obj.language == "javascript":
            return self._js(obj.path)
        return {"status": "no analyzer"}

    def _py(self, path):
        code = open(path).read()
        return {
            "imports": re.findall(r"^import .*|^from .* import .*", code, re.M),
            "functions": re.findall(r"def (.*?)\(", code)
        }

    def _js(self, path):
        code = open(path).read()
        return {
            "imports": re.findall(r"import .* from .*", code),
            "functions": re.findall(r"function (.*?)\(", code)
        }


class QExecutor:
    def run(self, obj: QObject):
        if obj.language == "python":
            subprocess.run(["python", obj.path])
        elif obj.language == "javascript":
            subprocess.run(["node", obj.path])


class QEngine:
    def __init__(self):
        self.detector = QDetector()
        self.analyzer = QAnalyzer()
        self.executor = QExecutor()

    def understand(self, path):
        obj = self.detector.detect(path)
        analysis = self.analyzer.analyze(obj)
        return {
            "object": obj.__dict__,
            "analysis": analysis
        }

    def run(self, path):
        obj = self.detector.detect(path)
        return self.executor.run(obj)
