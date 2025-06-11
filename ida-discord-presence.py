import time
import logging
import ida_idaapi
import ida_kernwin
import ida_funcs
import ida_nalt
from typing import TypedDict, Optional
from pypresence import Presence

# ==== TYPES ====
class ConfigDict(TypedDict):
    client_id: str
    enabled: bool
    update_interval: int
    display_options: dict[str, bool] 
    texts: dict[str, str] 


# ==== CONSTANTS ====
CONFIG: ConfigDict = {
    "client_id": "1227589006905049132",
    "enabled": True,
    "update_interval": 15,
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
    "debug": False
}

# ==== END OF CONFIG MANAGER ====

if CONFIG.get("debug", False):
    log_level = logging.INFO
else:
    log_level = logging.ERROR

logging.basicConfig(
    level=log_level, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DiscordRPC")

class DiscordRPCHandler:
    def __init__(self):
        self._RPC = Presence(CONFIG["client_id"])

        if not self._RPC:
            raise ValueError("Failed to initialize Discord RPC Presence")
        
        self.connect()
        
    
    def connect(self) -> bool:
        try:
            self._RPC.connect()
            logger.info("Connected to Discord RPC")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Discord RPC: {e}")
            return False
    
    def update(
        self,
        filename: Optional[str] = None,
        function_name: Optional[str] = None
    ) -> bool:
        try:
            if not hasattr(self._RPC, 'connected') or not self._RPC.connected:
                logger.warning("Discord RPC not connected, attempting to reconnect...")
            if not self.connect():
                logger.error("Failed to reconnect to Discord RPC")
                return False
            
            state_template = CONFIG["texts"]["state_template"]
            details_template = CONFIG["texts"]["details_template"]
            
            state = state_template.format(filename=filename or "unknown")
            details = details_template.format(function_name=function_name or "unknown")
            
            self._RPC.update(
                state=state,
                details=details,
                large_image=None,
                small_image=None,
                start=int(time.time())
            )
            return True
        except Exception as e:
            logger.error(f"Failed to update Discord RPC: {e}")
            if "Event loop is closed" in str(e):
                logger.info("Attempting to reconnect due to closed event loop")
                try:
                    self.connect()
                except Exception:
                    pass  
            return False

# ==== END OF DISCORD RPC MANAGER ====

class DiscordPresencePlugin(ida_idaapi.plugin_t):
    flags = ida_idaapi.PLUGIN_KEEP
    comment = "Shows your IDA activity in Discord"
    help = "Discord Rich Presence for IDA Pro"
    wanted_name = "Discord Rich Presence"
    wanted_hotkey = ""
    
    def __init__(self):
        self.discord = None 

    def _update_timer_callback(self):
        try:
            if not hasattr(self, 'discord') or not self.discord:
                return -1 
                
            ea = ida_kernwin.get_screen_ea()
            func = ida_funcs.get_func(ea)
            
            if func:
                function_name = ida_funcs.get_func_name(func.start_ea) or "unnamed"
            else:
                function_name = "unknown"
                
            filename = ida_nalt.get_root_filename() or "unknown"

            if self.last_function_name != function_name:
                self.last_function_name = function_name
                self.discord.update(filename=filename, function_name=function_name)
                logger.info(f"File changed: {function_name}")

            return CONFIG["update_interval"] * 1000
        except Exception as e:
            logger.error(f"Timer update error: {e}")
            return -1 
    
    def init(self):
        try:
            self.discord = DiscordRPCHandler()
            
            filename = ida_nalt.get_root_filename() or "unknown_file"
            ea = ida_kernwin.get_screen_ea()
            func = ida_funcs.get_func(ea)
            function_name = ida_funcs.get_func_name(func.start_ea) if func else "unknown"

            self.last_function_name = filename
            self.discord.update(filename=filename, function_name=function_name)

            self.timer_id = ida_kernwin.register_timer(
                CONFIG["update_interval"] * 1000,  # 15000 мс = 15 секунд
                self._update_timer_callback
            )
            
            logger.info("Discord Rich Presence initialized")
            return ida_idaapi.PLUGIN_OK
        except Exception as e:
            logger.error(f"Failed to initialize Discord Rich Presence: {e}")
            return ida_idaapi.PLUGIN_SKIP
    
    def run(self):
        ida_kernwin.info("Discord Rich Presence is active")
    
    def term(self):
        try:
            if hasattr(self, 'discord') and self.discord:
                self.discord._RPC.close()
                
            if hasattr(self, 'ui_hooks') and self.ui_hooks:
                self.ui_hooks.unhook()
                
            if hasattr(self, 'ui_hooks') and hasattr(self.ui_hooks, 'ida_hooks'):
                self.ui_hooks.ida_hooks.unhook()
        except Exception as e:
            logger.error(f"Error during plugin termination: {e}")


def PLUGIN_ENTRY():
    return DiscordPresencePlugin()