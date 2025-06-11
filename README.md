# IDA Discord Presence

![Discord Rich Presence](https://img.shields.io/badge/Discord-Rich%20Presence-7289DA?logo=discord)

A plugin that displays your IDA Pro activity in Discord using Rich Presence. Show your colleagues what you're currently reversing!

## Features

- Shows the name of the file you're analyzing
- Displays the current function you're examining
- Automatically updates your Discord status
- Configurable update intervals
- Minimal performance impact on IDA Pro

## Screenshots

<img width="272" alt="Screenshot 2025-06-11 at 11 42 17" src="https://github.com/user-attachments/assets/3dc418f9-c7d0-4a4d-84a5-6e131dcbe6a7" />

## Requirements

- IDA Pro 9.1 or compatible version
- Discord desktop client running on the same machine
- Python 3.6+ with required packages

## Installation

1. Clone this repository or download the files

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy ida-discord-presence.py to your IDA plugins directory:
   - Windows: `%APPDATA%\Hex-Rays\IDA Pro\plugins\`
   - macOS: `~/Library/Application Support/IDA Pro/plugins/`
   - Linux: `~/.idapro/plugins/`
4. Rename the file to `discord_presence.py` (optional but recommended)
5. Start IDA Pro

## Configuration

The plugin can be configured by modifying the `CONFIG` dictionary in the script:

```python
CONFIG: ConfigDict = {
    "client_id": "1227589006905049132",  # Discord application ID
    "enabled": True,                     # Enable/disable the plugin
    "update_interval": 15,               # Update interval in seconds
    "display_options": {
        "show_filename": True,
        "show_function_name": True,
        "show_address": True,
        "show_elapsed_time": True
    },
    "texts": {
        "state_template": "Analyzing {filename}",
        "details_template": "Function: {function_name}",
        "large_text": "IDA Pro",
        "small_text": "Reversing"
    },
    "debug": False                      # Enable debug logging
}
```

## Troubleshooting

If you encounter issues:

1. Enable debug mode by setting `"debug": True` in the CONFIG
2. Check the IDA Pro output window for error messages
3. If Discord is not detecting the plugin, ensure:
   - Discord is running and you're logged in
   - You're not set to "Invisible" in Discord
   - Discord has game activity enabled in User Settings > Activity Status

## Known Issues

- May occasionally disconnect from Discord and require restarting IDA Pro
- Limited customization in current version

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- Developed by localpulse 
- Uses the [pypresence](https://github.com/qwertyquerty/pypresence) library
