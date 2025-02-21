# 🐍 PyShell

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)

A lightweight, extensible shell implementation written in Python that provides core Unix-like shell functionality with built-in command support and tab completion.

## ✨ Features

- **Built-in Commands**: Implements essential shell commands like `cd`, `pwd`, `echo`, and `type`
- **Tab Completion**: Smart context-aware tab completion for commands and file paths
- **External Command Support**: Seamlessly execute external system commands
- **Path Resolution**: Intelligent PATH-based command resolution
- **Error Handling**: Robust error handling for file operations and command execution
- **Cross-Platform**: Works on Unix-like systems and Windows

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- No external dependencies required!

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pyshell.git
cd pyshell
```

2. Make the script executable (Unix-like systems):
```bash
chmod +x pyshell.py
```

3. Run PyShell:
```bash
./pyshell.py
```

## 💡 Usage

Once PyShell is running, you'll see the shell prompt `$`. Here are some examples of what you can do:

```bash
$ pwd                    # Print working directory
/home/user/projects

$ cd Documents          # Change directory
$ echo Hello World      # Print text
Hello World

$ type echo            # Check command type
echo is a shell builtin

$ ls                    # Run external commands
file1.txt file2.txt
```

### Built-in Commands

| Command | Description |
|---------|-------------|
| `cd [dir]` | Change current directory (defaults to home directory if no argument) |
| `pwd` | Print working directory |
| `echo [text...]` | Print text to standard output |
| `type [command]` | Display command type (builtin or external) |
| `exit [code]` | Exit shell with optional status code |

## 🔧 Architecture

PyShell is built with a modular, object-oriented design:

- `Shell`: Main shell class handling input processing and command execution
- `ShellCommand`: Abstract base class for all built-in commands
- `PathResolver`: Handles command path resolution using system PATH
- `Completer`: Provides context-aware tab completion functionality

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. 🐛 Report bugs
2. 🎈 Request features
3. 📝 Submit pull requests
4. 📖 Improve documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Future Improvements

- [ ] Command history support
- [ ] Pipeline implementation
- [ ] Environment variable management
- [ ] Shell scripting support
- [ ] Alias support
- [ ] More built-in commands

## 📞 Contact

If you have any questions or suggestions, feel free to open an issue or reach out directly.

---

Made with ❤️ using Python
