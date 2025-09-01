# system_monitor.py (v2.0 - The Omega Prime "World No. 1" Guardian)

import threading
import time
import logging
import psutil
import os
import socket
from datetime import datetime, timedelta

# --- कांसेप्चुअल इम्पोर्टहरू (यी मोड्युलहरू बनेपछि काम गर्नेछ) ---
# from config import SYSTEM_MONITOR_CONFIG, is_configured_correctly
# from email_system import EmailService

# --- अस्थायी कन्फिगरेसन (config.py बनेपछि त्यहाँ सारिनेछ) ---
# TODO: Move these to config.py
SYSTEM_MONITOR_CONFIG = {
    "interval_seconds": 300,  # 5 minutes
    "cpu_warn_percent": 80.0,
    "cpu_crit_percent": 95.0,
    "mem_warn_percent": 80.0,
    "mem_crit_percent": 90.0,
    "disk_warn_percent": 85.0,
    "disk_crit_percent": 95.0,
    "app_mem_limit_mb": 2048,  # 2GB limit for the AI process
    "heartbeat_timeout_seconds": 1800 # 30 minutes
}

class SystemMonitor:
    """
    उद्देश्य #6 (रीयल-टाइम मोनिटरिंग) र #2 (स्व-मर्मत) को लागि एक सक्रिय र बुद्धिमान संरक्षक।
    यो प्रणालीको स्वास्थ्य, एप्लिकेसनको अवस्था, र नेटवर्क जडानको निगरानी गर्दछ।
    गम्भीर समस्याहरूमा, यसले इमेल मार्फत चेतावनी पठाउन सक्छ।
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SystemMonitor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # यो सुनिश्चित गर्दछ कि __init__ एक पटक मात्र चल्छ (Singleton Pattern)
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        self.logger = logging.getLogger(__name__)
        self.monitoring_active = True
        self.last_heartbeat = datetime.now()
        self.process = psutil.Process(os.getpid())
        
        # Daemon थ्रेडले मुख्य कार्यक्रम बन्द हुँदा स्वतः बन्द हुन्छ
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.logger.info("Omega Prime Guardian (v2.0) प्रारम्भ भयो।")

    def start(self):
        """मुख्य कार्यक्रमद्वारा कल गरिने: पृष्ठभूमिमा निगरानी सुरु गर्दछ।"""
        if not self.monitor_thread.is_alive():
            self.logger.info("सिस्टम गार्डियन थ्रेड सुरु गर्दै।")
            self.monitor_thread.start()

    def stop(self):
        """निगरानी लूप रोक्छ।"""
        self.logger.info("सिस्टम गार्डियन थ्रेड रोक्दै।")
        self.monitoring_active = False

    def update_heartbeat(self):
        """(उद्देश्य #2) main.py ले यो प्रकार्यलाई कल गरेर आफू जीवित रहेको संकेत दिन्छ।"""
        self.last_heartbeat = datetime.now()
        self.logger.debug("हार्टबिट प्राप्त भयो। मुख्य लूप सक्रिय छ।")

    def _send_critical_alert(self, subject, message):
        """(उद्देश्य #33) इमेल प्रणाली मार्फत गम्भीर चेतावनी पठाउँछ।"""
        self.logger.critical(f"ALERT TRIGGERED: {subject} - {message}")
        # TODO: email_system.py बनेपछि वास्तविक इमेल पठाउने कोड यहाँ राख्ने।
        # try:
        #     from config import EMAIL_CONFIG
        #     email_service = EmailService(...)
        #     email_service.send_text_email(EMAIL_CONFIG['default_recipient'], f"🛡️ OMEGA PRIME SYSTEM ALERT: {subject}", message)
        #     self.logger.info("गम्भीर प्रणाली चेतावनी सफलतापूर्वक पठाइयो।")
        # except Exception as e:
        #     self.logger.error(f"प्रणाली चेतावनी इमेल पठाउन असफल: {e}")
        print(f"--- CRITICAL EMAIL ALERT (SIMULATED) ---\nSUBJECT: {subject}\nMESSAGE: {message}\n-----------------------------------------")


    def _monitor_loop(self):
        """मुख्य लूप जसले प्रणालीको हरेक पक्षको जाँच गर्दछ।"""
        self.logger.info(f"गार्डियन निगरानी लूप सुरु भयो। अन्तराल: {SYSTEM_MONITOR_CONFIG['interval_seconds']} सेकेन्ड।")
        
        while self.monitoring_active:
            # १. प्रणाली स्रोत जाँच (CPU, RAM, Disk)
            cpu_usage = psutil.cpu_percent(interval=1)
            mem_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')
            
            if cpu_usage > SYSTEM_MONITOR_CONFIG['cpu_crit_percent']:
                self._send_critical_alert("CPU Usage CRITICAL", f"CPU usage is at {cpu_usage}%, exceeding the {SYSTEM_MONITOR_CONFIG['cpu_crit_percent']}% threshold.")
            elif cpu_usage > SYSTEM_MONITOR_CONFIG['cpu_warn_percent']:
                self.logger.warning(f"CPU usage HIGH: {cpu_usage}%")

            if mem_info.percent > SYSTEM_MONITOR_CONFIG['mem_crit_percent']:
                 self._send_critical_alert("Memory Usage CRITICAL", f"System memory usage is at {mem_info.percent}%, exceeding the {SYSTEM_MONITOR_CONFIG['mem_crit_percent']}% threshold.")
            elif mem_info.percent > SYSTEM_MONITOR_CONFIG['mem_warn_percent']:
                self.logger.warning(f"System memory usage HIGH: {mem_info.percent}%")

            # २. एप्लिकेसन स्वास्थ्य जाँच (App Memory, Heartbeat)
            app_mem_mb = self.process.memory_info().rss / (1024 * 1024)
            if app_mem_mb > SYSTEM_MONITOR_CONFIG['app_mem_limit_mb']:
                self._send_critical_alert("Application Memory CRITICAL", f"Omega Prime is consuming {app_mem_mb:.2f} MB of memory, exceeding the limit of {SYSTEM_MONITOR_CONFIG['app_mem_limit_mb']} MB. Possible memory leak.")

            time_since_heartbeat = datetime.now() - self.last_heartbeat
            if time_since_heartbeat > timedelta(seconds=SYSTEM_MONITOR_CONFIG['heartbeat_timeout_seconds']):
                self._send_critical_alert("Application HANG Detected", f"No heartbeat received for {time_since_heartbeat.total_seconds():.0f} seconds. The main process may be frozen or crashed. Initiating self-healing protocol is advised.")
                # (उद्देश्य #2) भविष्यमा, यहाँ स्वतः पुनः सुरु गर्ने कोड राख्न सकिन्छ।
                # from main import restart_program; restart_program()

            # ३. नेटवर्क जडान जाँच
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=5) # गुगलको DNS मा जडान गर्ने प्रयास
                network_ok = True
            except OSError:
                network_ok = False
                self._send_critical_alert("Network Connectivity LOST", "Cannot connect to the internet (8.8.8.8). Omega Prime is operating blind.")

            self.logger.info(f"स्वास्थ्य जाँच - CPU: {cpu_usage}%, SysMem: {mem_info.percent}%, AppMem: {app_mem_mb:.2f}MB, Network: {'OK' if network_ok else 'FAIL'}")
            time.sleep(SYSTEM_MONITOR_CONFIG['interval_seconds'])


# --- आत्म-परीक्षण ब्लक (यो फाइल सीधै चलाएर परीक्षण गर्न) ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    print("Omega Prime Guardian (v2.0) को स्ट्यान्डअलोन परीक्षण चलिरहेको छ...")
    
    # छिटो जाँचको लागि अन्तराल ओभरराइड गर्नुहोस्
    SYSTEM_MONITOR_CONFIG['interval_seconds'] = 10
    SYSTEM_MONITOR_CONFIG['heartbeat_timeout_seconds'] = 20
    
    monitor = SystemMonitor()
    monitor.start()
    
    try:
        print("पहिलो १५ सेकेन्डको लागि हार्टबिट पठाइँदै...")
        for i in range(3):
            time.sleep(5)
            monitor.update_heartbeat()
            print(f"[{datetime.now()}] Heartbeat sent.")
        
        print("\nअब ३० सेकेन्डको लागि हार्टबिट रोकिँदै, ह्याङ्ग पत्ता लगाउने परीक्षण गर्न...")
        time.sleep(30)

    except KeyboardInterrupt:
        print("\nप्रयोगकर्ताद्वारा परीक्षण रोकियो।")
    finally:
        monitor.stop()
        print("स्ट्यान्डअलोन परीक्षण समाप्त भयो।")
