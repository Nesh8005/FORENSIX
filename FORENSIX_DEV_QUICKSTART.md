# 🚀 FORENSIX SENTINEL - QUICK START FOR DEVELOPERS

**Get your dev team started in 30 minutes!**

---

## 📦 **COMPLETE PACKAGE FILES**

You now have these documents:

1. **FORENSIX_README.md** - Overview and package contents
2. **FORENSIX_SPECIFICATION.md** - Complete technical spec (100+ pages worth)
3. **FORENSIX_IMPLEMENTATION_PLAN.md** - 12-week roadmap with daily tasks
4. **FORENSIX_REQUIREMENTS.txt** - All dependencies
5. **THIS FILE** - Quick start guide

---

## 🎯 **30-MINUTE ONBOARDING**

### **Step 1: Read This First** (5 min)

- This file (you're reading it!)
- FORENSIX_README.md

### **Step 2: Understand Architecture** (10 min)

- FORENSIX_SPECIFICATION.md (Section 2: Architecture)
- Review high-level diagram
- Understand module breakdown

### **Step 3: Check Implementation Plan** (10 min)

- FORENSIX_IMPLEMENTATION_PLAN.md (Sprint 1)
- Understand your role(assignments)
- Review first week tasks

### **Step 4: Setup Environment** (5 min)

- Follow environment setup below

---

## 💻 **DEVELOPMENT ENVIRONMENT SETUP**

### **Prerequisites**

```bash
# Kali Linux 2023+ (recommended)
# OR Ubuntu 22.04+
# OR macOS 13+

# Python 3.10+
python3 --version  # Must be >= 3.10

# Git
git --version
```

### **Quick Setup Script**

```bash
# 1. Clone repository (once created)
git clone https://github.com/YOUR_ORG/forensix-sentinel.git
cd forensix-sentinel

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download AI models
python -m spacy download en_core_web_sm

# 5. Install system tools (Kali/Ubuntu)
sudo apt update
sudo apt install -y \
    exiftool \
    binwalk \
    foremost \
    volatility3 \
    wireshark-common

# 6. Verify installation
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import spacy; print('spaCy:', spacy.__version__)"

# 7. Run tests (once code exists)
pytest tests/
```

### **IDE Setup**

**Recommended: VS Code**

```bash
# Install VS Code extensions
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-toolsai.jupyter

# Open project
code .
```

**VS Code settings (.vscode/settings.json):**

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

---

## 📁 **INITIAL PROJECT STRUCTURE**

```
forensix-sentinel/
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
│
├── forensix/
│   ├── __init__.py
│   ├── cli.py              # START HERE - Dev 1
│   ├── orchestrator.py
│   │
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── file_analyzer.py     # Dev 1
│   │   ├── disk_forensics.py    # Dev 3
│   │   ├── network_forensics.py # Dev 3
│   │   ├── log_analyzer.py      # Dev 3
│   │   ├── ai_engine.py         # Dev 2
│   │   ├── correlation.py       # All (Week 6+)
│   │   └── reporting.py         # All (Week 11+)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── hashing.py
│   │   ├── strings.py
│   │   └── validators.py
│   │
│   └── config/
│       ├── __init__.py
│       └── settings.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── docs/
│   └── API.md
│
└── scripts/
    └── setup.sh
```

---

## 👥 **TEAM ASSIGNMENTS**

### **Developer 1: Lead + File Analysis**

**Sprint 1 Priority Tasks:**

1. Create project structure ✅
2. Implement CLI framework (Click) ✅
3. Build FileAnalyzer class ✅
4. Add magic byte detection ✅
5. Hash calculation (MD5, SHA, SSDeep) ✅

**Files to create:**

- `forensix/cli.py`
- `forensix/modules/file_analyzer.py`
- `forensix/utils/hashing.py`
- `tests/unit/test_file_analyzer.py`

**Sprint 1 Goal:** Working CLI that can scan files and calculate hashes

### **Developer 2: AI/ML Engineer**

**Sprint 1 Priority Tasks:**

1. Setup ML environment ✅
2. Configure spaCy NER ✅
3. Create entity models ✅
4. Collect CTF flag patterns ✅
5. Initial NER training ✅

**Files to create:**

- `forensix/modules/ai_engine.py`
- `forensix/ai/flag_detector.py`
- `forensix/ai/models/` (directory for models)
- `tests/unit/test_ai_engine.py`

**Sprint 1 Goal:** Basic NER working with entity extraction

### **Developer 3: Forensics Specialist**

**Sprint 1 Priority Tasks:**

1. Install forensics tools ✅
2. Test pytsk3 integration ✅
3. Create log parsers POC ✅
4. Timeline data structures ✅
5. Integration planning ✅

**Files to create:**

- `forensix/modules/disk_forensics.py`
- `forensix/modules/log_analyzer.py`
- `forensix/utils/timeline.py`
- `tests/unit/test_log_analyzer.py`

**Sprint 1 Goal:** Basic log parsing and timeline structure

---

## 🔧 **DEVELOPMENT WORKFLOW**

### **Git Workflow**

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes and commit often
git add .
git commit -m "feat(module): add functionality"

# 3. Push to remote
git push origin feature/your-feature-name

# 4. Create Pull Request on GitHub
# 5. Wait for code review
# 6. Merge after approval
```

### **Commit Message Format**

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Add tests
- `chore`: Maintenance

**Examples:**

```
feat(file-analyzer): add PDF parsing support
fix(ai-engine): correct flag detection regex
docs(api): update FileAnalyzer documentation
test(hashing): add SSDeep test cases
```

### **Code Review Checklist**

Before submitting PR:

- [ ] Code follows PEP 8
- [ ] All tests pass
- [ ] New tests added for new code
- [ ] Docstrings updated
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] Type hints added

---

## 🧪 **TESTING**

### **Run Tests**

```bash
# All tests
pytest

# With coverage
pytest --cov=forensix --cov-report=html

# Specific module
pytest tests/unit/test_file_analyzer.py

# View coverage report
open htmlcov/index.html
```

### **Writing Tests**

```python
# tests/unit/test_file_analyzer.py

import pytest
from forensix.modules.file_analyzer import FileAnalyzer

def test_hash_calculation():
    """Test MD5 hash calculation"""
    analyzer = FileAnalyzer()
    result = analyzer.calculate_hash("tests/fixtures/test.txt", "md5")
    assert result == "expected_hash_value"

def test_file_type_detection():
    """Test magic byte detection"""
    analyzer = FileAnalyzer()
    file_type = analyzer.detect_type("tests/fixtures/image.jpg")
    assert file_type == "image/jpeg"
```

---

## 📋 **SPRINT 1 CHECKLIST**

### **Week 1**

**All Team:**

- [ ] Environment setup complete
- [ ] Git repository cloned
- [ ] All dependencies installed
- [ ] Can run `pytest` successfully

**Dev 1:**

- [ ] Project structure created
- [ ] CLI framework implemented
- [ ] FileAnalyzer class created
- [ ] Magic byte detection working

**Dev 2:**

- [ ] ML environment configured
- [ ] spaCy installed and tested
- [ ] NER pipeline created
- [ ] Pattern collection started

**Dev 3:**

- [ ] Forensics tools installed
- [ ] pytsk3 tested
- [ ] Log parser POC created
- [ ] Timeline structures defined

### **Week 2**

**All Team:**

- [ ] Integration testing
- [ ] Code reviews completed
- [ ] Sprint 1 demo prepared

**Dev 1:**

- [ ] Hash calculation complete
- [ ] String extraction working
- [ ] Archive handling (ZIP)
- [ ] Unit tests >= 50% coverage

**Dev 2:**

- [ ] NER model trained
- [ ] Entity extraction working
- [ ] Scoring algorithm implemented
- [ ] Model persistence added

**Dev 3:**

- [ ] Event log parsing
- [ ] Syslog parsing
- [ ] Timeline correlation POC
- [ ] Integration tests

---

## 🐛 **TROUBLESHOOTING**

### **Common Issues**

**Issue: `ImportError: No module named 'pytsk3'`**

```bash
# Install system dependencies first
sudo apt install libtsk-dev
pip install pytsk3
```

**Issue: `CUDA not available`**

```bash
# Check CUDA installation
nvidia-smi

# Install PyTorch with CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

**Issue: `Permission denied` for forensics tools**

```bash
# Add user to necessary groups
sudo usermod -a -G disk $USER
# Logout and login again
```

**Issue: Tests failing**

```bash
# Clear pytest cache
pytest --cache-clear

# Run with verbose output
pytest -v

# Run specific test
pytest tests/unit/test_file_analyzer.py::test_hash_calculation -v
```

---

## 📞 **COMMUNICATION**

### **Daily Standup Format**

1. What did you do yesterday?
2. What will you do today?
3. Any blockers?

### **Collaboration Tools**

- GitHub: Code, PRs, Issues
- Slack/Discord: Daily communication
- Zoom: Standup, reviews
- Notion/Confluence: Documentation

### **Getting Help**

- Check documentation first
- Search GitHub issues
- Ask in team chat
- Pair programming session

---

## 🎯 **SPRINT 1 GOALS (REMINDER)**

By end of Week 2, we MUST have:

✅ Working CLI command
✅ File scanning capability
✅ Hash calculation
✅ Basic AI/NER
✅ Log parsing POC
✅ >= 50% test coverage
✅ Core architecture validated

**MVP Demo:** Scan a file → Extract entities → Output report

---

## 📚 **ESSENTIAL READING**

### **Before You Start:**

1. FORENSIX_SPECIFICATION.md (Sections 1-3)
2. FORENSIX_IMPLEMENTATION_PLAN.md (Sprint 1)
3. This file

### **Reference Documents:**

- Python PEP 8: <https://peps.python.org/pep-0008/>
- Click Documentation: <https://click.palletsprojects.com/>
- PyTorch Tutorials: <https://pytorch.org/tutorials/>
- spaCy Guide: <https://spacy.io/usage>

### **Forensics Resources:**

- Digital Forensics Discord
- SANS Forensics Blog
- Autopsy Documentation
- Volatility  Wiki

---

## 🚀 **LET'S GO!**

You now have everything you need to start building Forensix Sentinel!

**Next Steps:**

1. ✅ Setup environment (30 min)
2. ✅ Review Sprint 1 tasks (15 min)
3. ✅ Create initial code structure (1 hour)
4. ✅ Start coding! 🔥

**First Commit Target:** End of Day 1

**First Demo:** End of Week 2

**V1.0 Launch:** Week 12

---

## 💬 **Questions?**

Refer to:

- FORENSIX_SPECIFICATION.md for technical details
- FORENSIX_IMPLEMENTATION_PLAN.md for task breakdown
- Team lead for clarification

---

**WELCOME TO THE TEAM! LET'S BUILD SOMETHING AMAZING! 🐉🔍🔥**
