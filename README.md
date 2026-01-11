# Edu Mail Generator - Modernized Version

🎓 **Generate Educational Email Accounts Automatically**

A modernized, Windows-compatible version of the educational email generator with GitHub Secrets support and improved reliability.

## ✨ Features

- 🔧 **Modern Selenium 4.x** - Updated to latest Selenium with proper WebDriver management
- 🪟 **Windows Compatible** - Full Windows support with automatic driver management
- 🔐 **GitHub Secrets Integration** - Secure credential management via environment variables
- 🤖 **Undetected Chrome** - Bypass detection with undetected-chromedriver
- 📝 **Better Logging** - Comprehensive logging and error handling
- ⚙️ **Configuration Management** - JSON-based configuration system
- 🚀 **GitHub Actions Ready** - Automated execution via GitHub Actions
- 🛡️ **Error Recovery** - Robust error handling and retry mechanisms

## 🚀 Quick Start

### Method 1: Modern Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/hugetiny/Edu-Mail-Generator.git
cd Edu-Mail-Generator

# Run modern setup
python setup_modern.py

# Configure your email (copy and edit)
cp .env.example .env
# Edit .env file with your email

# Run the generator
python edu_mail_generator.py
```
## 📋 Requirements

- **Python 3.8+** (3.11+ recommended)
- **Google Chrome** or **Mozilla Firefox**
- **Windows 10/11**, **macOS**, or **Linux**

## 🔧 Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```env
# Your contact email
EDU_EMAIL=your-email@example.com

# Optional: GitHub email for Actions
GITHUB_EMAIL=your-github-email@example.com

# Optional: Custom settings
OUTPUT_FILE=generated_accounts.txt
LOG_LEVEL=INFO
```

### GitHub Secrets (for Actions)

Add these secrets to your GitHub repository:

- `EDU_EMAIL` - Your email address
- `GITHUB_EMAIL` - Alternative email (optional)

## 🎯 Usage

### Local Execution

```bash
# Interactive mode
python edu_mail_generator.py

```

### GitHub Actions

1. Go to your repository's **Actions** tab
2. Select **Edu Mail Generator** workflow
3. Click **Run workflow**
4. Choose college ID (1-5) and options
5. Download generated accounts from artifacts

## 🏫 Available Colleges

1. **MSJC College** (ID: 1)
2. **Contra Costa College** (ID: 2)
3. **City College** (ID: 3)
4. **Sacramento College** (ID: 4)
5. **Mt San Antonio** (ID: 5)

## 📁 Output

Generated accounts are saved to:
- `generated_accounts.txt` - Account details
- `edu_generator.log` - Execution logs

## ⚠️ Important Notes

- **Educational Purpose Only** - Use responsibly and ethically
- **Rate Limiting** - Don't abuse the service
- **Captcha Required** - Manual captcha solving needed
- **No Guarantees** - Success depends on target site availability

## 🔍 Troubleshooting

### Common Issues

1. **Browser not found**
   ```bash
   # Install Chrome or Firefox
   # Run setup again
   python setup_modern.py
   ```

2. **Selenium errors**
   ```bash
   # Update dependencies
   pip install -r requirements.txt --upgrade
   ```

3. **Windows path issues**
   ```bash
   # Use forward slashes in paths
   # Run as administrator if needed
   ```
# tjopp
# tjopp

