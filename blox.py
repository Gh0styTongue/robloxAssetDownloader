import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import requests
import os
import re
import threading
import configparser
import json
from datetime import datetime

class RobloxAssetDownloader(tk.Tk):
    """
    A 1:1 Python conversion of the Roblox Asset Downloader Electron application.
    This application allows for downloading of Roblox assets, including private assets,
    with a graphical user interface built using Tkinter.
    Includes advanced handling for M3U8 video playlists.
    """
    def __init__(self):
        super().__init__()
        self.title("Roblox Asset Downloader")
        self.geometry("400x480")
        self.resizable(False, False)

        self.config_path, self.log_path = self.get_paths()
        self.setup_logging()

        self.config = configparser.ConfigParser()
        self.load_settings()

        self.style = ttk.Style(self)
        self.apply_styles()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=(10, 0))

        self.individual_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.individual_frame, text="Individual Download")
        self.create_individual_widgets()

        self.bulk_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.bulk_frame, text="Bulk Download")
        self.create_bulk_widgets()

        self.settings_button = ttk.Button(self, text="Settings", command=self.open_settings)
        self.settings_button.pack(pady=10)

        self.load_saved_cookie()
        self.log("Application initialized successfully.")

    def get_paths(self):
        appdata_path = os.getenv('APPDATA') or os.path.expanduser("~")
        config_dir = os.path.join(appdata_path, "RobloxAssetDownloader")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "settings.ini"), config_dir

    def setup_logging(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = os.path.join(self.log_path, f"log_{timestamp}.txt")

    def log(self, message):
        print(message)
        with open(self.log_file, "a") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

    def load_settings(self):
        self.log("Loading settings from settings.ini.")
        self.config.read(self.config_path)
        if not self.config.has_section('Theme'):
            self.config.add_section('Theme')
            self.config.set('Theme', 'background', '#ffffff')
            self.config.set('Theme', 'tab_background', '#f1f5f9')
            self.config.set('Theme', 'button_background', '#3b82f6')
            self.config.set('Theme', 'button_active', '#2563eb')
            self.config.set('Theme', 'button_text', '#ffffff')
        if not self.config.has_section('User'):
            self.config.add_section('User')
            self.config.set('User', 'roblosecurity', '')

    def save_settings(self):
        self.log("Saving settings to settings.ini.")
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)
        self.apply_styles()

    def load_saved_cookie(self):
        saved_cookie = self.config.get('User', 'roblosecurity', fallback='')
        if saved_cookie:
            self.log("Loaded saved .ROBLOSECURITY cookie.")
            self.individual_cookie_entry.delete(0, tk.END)
            self.individual_cookie_entry.insert(0, saved_cookie)
            self.bulk_cookie_entry.delete(0, tk.END)
            self.bulk_cookie_entry.insert(0, saved_cookie)

    def apply_styles(self):
        self.log("Applying UI styles.")
        theme = self.config['Theme']
        self.configure(bg=theme.get('tab_background', '#f1f5f9'))
        self.style.theme_use('clam')

        self.style.configure("TNotebook", background=theme.get('tab_background', '#f1f5f9'), borderwidth=0)
        self.style.configure("TNotebook.Tab", background=theme.get('tab_background', '#e2e8f0'), padding=[10, 5], font=('Helvetica', 10, 'bold'))
        self.style.map("TNotebook.Tab", background=[("selected", theme.get('button_background', '#3b82f6'))], foreground=[("selected", theme.get('button_text', 'white'))])
        self.style.configure("TFrame", background=theme.get('background', 'white'))
        self.style.configure("TLabel", background=theme.get('background', 'white'), font=('Helvetica', 10))
        self.style.configure("TEntry", padding=5, font=('Helvetica', 10))
        self.style.configure("TButton", background=theme.get('button_background', '#3b82f6'), foreground=theme.get('button_text', 'white'), font=('Helvetica', 10, 'bold'), padding=8)
        self.style.map("TButton", background=[("active", theme.get('button_active', '#2563eb'))])

    def create_individual_widgets(self):
        ttk.Label(self.individual_frame, text="Asset Downloader", font=("Helvetica", 18, "bold")).pack(pady=(0, 20))
        ttk.Label(self.individual_frame, text="Roblox Cookie").pack(anchor="w", pady=(0, 2))
        self.individual_cookie_entry = ttk.Entry(self.individual_frame, show="*", width=40)
        self.individual_cookie_entry.pack(fill="x", pady=(0, 10))
        ttk.Label(self.individual_frame, text="Place ID").pack(anchor="w", pady=(0, 2))
        self.individual_place_id_entry = ttk.Entry(self.individual_frame, width=40)
        self.individual_place_id_entry.pack(fill="x", pady=(0, 10))
        ttk.Label(self.individual_frame, text="Asset ID").pack(anchor="w", pady=(0, 2))
        self.individual_asset_id_entry = ttk.Entry(self.individual_frame, width=40)
        self.individual_asset_id_entry.pack(fill="x", pady=(0, 20))
        self.individual_download_button = ttk.Button(self.individual_frame, text="Download", command=self.start_individual_download)
        self.individual_download_button.pack(fill="x")

    def create_bulk_widgets(self):
        ttk.Label(self.bulk_frame, text="Bulk Asset Downloader", font=("Helvetica", 18, "bold")).pack(pady=(0, 20))
        ttk.Label(self.bulk_frame, text="Roblox Cookie").pack(anchor="w", pady=(0, 2))
        self.bulk_cookie_entry = ttk.Entry(self.bulk_frame, show="*", width=40)
        self.bulk_cookie_entry.pack(fill="x", pady=(0, 10))
        ttk.Label(self.bulk_frame, text="Place IDs (one per line)").pack(anchor="w", pady=(0, 2))
        self.bulk_place_ids_text = tk.Text(self.bulk_frame, height=3, relief="solid", borderwidth=1, font=('Helvetica', 10))
        self.bulk_place_ids_text.pack(fill="x", pady=(0, 10))
        ttk.Label(self.bulk_frame, text="Asset IDs (one per line)").pack(anchor="w", pady=(0, 2))
        self.bulk_asset_ids_text = tk.Text(self.bulk_frame, height=5, relief="solid", borderwidth=1, font=('Helvetica', 10))
        self.bulk_asset_ids_text.pack(fill="x", pady=(0, 20))
        self.bulk_download_button = ttk.Button(self.bulk_frame, text="Download", command=self.start_bulk_download)
        self.bulk_download_button.pack(fill="x")

    def parse_id(self, id_str):
        parsed = re.sub(r'\D+', '', id_str)
        self.log(f"Parsed '{id_str}' to '{parsed}'.")
        return parsed

    def get_file_extension(self, data):
        try:
            magic_bytes = data[:8].decode('utf-8', errors='ignore')
            if magic_bytes == "<roblox!": return "rbxm"
            elif magic_bytes.startswith("<roblox"): return "rbxmx"
        except Exception: pass
        if data.startswith(b'\x89PNG\r\n\x1a\n'): return 'png'
        if data.startswith(b'\xFF\xD8\xFF'): return 'jpg'
        if data.startswith(b'GIF87a') or data.startswith(b'GIF89a'): return 'gif'
        if data.startswith(b'RIFF') and data[8:12] == b'WEBP': return 'webp'
        if data.startswith(b'OggS'): return 'ogg'
        if data.startswith(b'ID3'): return 'mp3'
        return "bin"

    def download_asset(self, asset_id, cookie, place_id):
        if not asset_id: return "Error: Asset ID cannot be empty."
        self.log(f"Starting download for Asset ID: {asset_id} with Place ID: {place_id or 'None'}")
        url = f"https://assetdelivery.roblox.com/v1/asset?id={asset_id}"
        headers = {"User-Agent": "Roblox/WinInet"}
        cookies = {}
        if cookie:
            cookies[".ROBLOSECURITY"] = cookie
            self.log("Using .ROBLOSECURITY cookie for request.")
        if place_id:
            headers["Roblox-Place-Id"] = place_id
            self.log(f"Using Roblox-Place-Id: {place_id} for request.")

        try:
            response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
            self.log(f"Initial request to {url} returned status code: {response.status_code}")
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    error_message = error_data.get('errors', [{}])[0].get('message', 'Unknown error')
                    error_code = error_data.get('errors', [{}])[0].get('code', 0)
                    self.log(f"API Error: {error_message}, Code: {error_code}")
                    return f"Error {response.status_code}: {error_message} (Code: {error_code})"
                except (json.JSONDecodeError, IndexError, KeyError):
                    self.log(f"HTTP Error: {response.status_code} - {response.reason}")
                    return f"Error {response.status_code}: {response.reason}"

            content = response.content
            text_content = content.decode('utf-8', errors='ignore')

            if text_content.strip().startswith("#EXTM3U") and "RBX-BASE-URI" in text_content:
                self.log("Detected M3U8 video master playlist. Handling video download.")
                return self.handle_video_playlist(asset_id, text_content, headers, cookies)
            else:
                extension = self.get_file_extension(content)
                self.log(f"Detected standard asset. Deduced extension: {extension}")
                downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
                os.makedirs(downloads_path, exist_ok=True)
                file_path = os.path.join(downloads_path, f"{asset_id}.{extension}")
                with open(file_path, "wb") as f: f.write(content)
                self.log(f"Asset successfully saved to {file_path}")
                return f"Success: Asset downloaded to {file_path}"

        except requests.Timeout:
            self.log("Request timed out.")
            return "Error: Download timed out after 10 seconds."
        except requests.RequestException as e:
            self.log(f"Network Error: {e}")
            return f"Error: An unexpected network error occurred: {e}"

    def handle_video_playlist(self, asset_id, playlist_content, headers, cookies):
        base_uri_match = re.search(r'#EXT-X-DEFINE:NAME="RBX-BASE-URI",VALUE="(.+?)"', playlist_content)
        if not base_uri_match:
            self.log("Could not find RBX-BASE-URI in video playlist.")
            return "Error: Could not parse video playlist (missing base URI)."
        base_uri = base_uri_match.group(1)
        self.log(f"Found base URI: {base_uri}")

        streams = re.findall(r'#EXT-X-STREAM-INF:.*?BANDWIDTH=(\d+).*?\n(.*?m3u8)', playlist_content)
        if not streams:
            self.log("Could not find any video streams in the master playlist.")
            return "Error: Could not parse video playlist (no streams found)."

        best_stream = max(streams, key=lambda item: int(item[0]))
        best_bandwidth, stream_path = best_stream
        stream_path = stream_path.replace('{$RBX-BASE-URI}', base_uri)
        self.log(f"Found best quality stream with bandwidth {best_bandwidth}: {stream_path}")

        media_playlist_url = stream_path
        self.log(f"Fetching media playlist from: {media_playlist_url}")
        media_response = requests.get(media_playlist_url, headers=headers, cookies=cookies)

        if media_response.status_code != 200:
            self.log(f"Failed to fetch media playlist. Status: {media_response.status_code}")
            return "Error: Failed to fetch video media playlist."

        video_segment_base_url = media_playlist_url.rsplit('/', 1)[0]
        final_video_url = f"{video_segment_base_url}/0000.webm"
        self.log(f"Constructed final video URL: {final_video_url}")
        
        video_response = requests.get(final_video_url, headers=headers, cookies=cookies)
        if video_response.status_code == 200:
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            file_path = os.path.join(downloads_path, f"{asset_id}.webm")
            with open(file_path, 'wb') as f:
                f.write(video_response.content)
            self.log(f"Video asset successfully saved to {file_path}")
            return f"Success: Video downloaded to {file_path}"
        else:
            self.log(f"Failed to download final video segment. Status: {video_response.status_code}")
            return "Error: Failed to download final video segment."

    def start_individual_download(self):
        self.individual_download_button.config(state="disabled", text="Downloading...")
        asset_id = self.parse_id(self.individual_asset_id_entry.get())
        cookie = self.individual_cookie_entry.get()
        place_id = self.parse_id(self.individual_place_id_entry.get())
        thread = threading.Thread(target=self.run_individual_download, args=(asset_id, cookie, place_id))
        thread.daemon = True
        thread.start()

    def run_individual_download(self, asset_id, cookie, place_id):
        result = self.download_asset(asset_id, cookie, place_id)
        if "Success" in result: messagebox.showinfo("Success", result)
        else: messagebox.showerror("Download Failed", result)
        self.individual_download_button.config(state="normal", text="Download")

    def start_bulk_download(self):
        self.bulk_download_button.config(state="disabled", text="Downloading...")
        cookie = self.bulk_cookie_entry.get()
        place_ids = [self.parse_id(line) for line in self.bulk_place_ids_text.get("1.0", "end-1c").splitlines() if line.strip()]
        asset_ids = [self.parse_id(line) for line in self.bulk_asset_ids_text.get("1.0", "end-1c").splitlines() if line.strip()]
        self.log(f"Starting bulk download for {len(asset_ids)} assets with {len(place_ids)} place IDs.")
        thread = threading.Thread(target=self.run_bulk_download, args=(asset_ids, cookie, place_ids))
        thread.daemon = True
        thread.start()

    def run_bulk_download(self, asset_ids, cookie, place_ids):
        failed_ids = []
        for asset_id in asset_ids:
            if not asset_id: continue
            success = False
            if not place_ids:
                result = self.download_asset(asset_id, cookie, None)
                if "Success" in result: success = True
            else:
                for place_id in place_ids:
                    result = self.download_asset(asset_id, cookie, place_id)
                    if "Success" in result:
                        success = True
                        break
            if not success: failed_ids.append(asset_id)
        
        if failed_ids:
            self.log(f"Bulk download finished with {len(failed_ids)} failures.")
            messagebox.showwarning("Bulk Download Complete", f"The following asset IDs failed to download:\n\n{', '.join(failed_ids)}")
        else:
            self.log("Bulk download finished successfully.")
            messagebox.showinfo("Bulk Download Complete", "All assets downloaded successfully.")
        self.bulk_download_button.config(state="normal", text="Download")

    def open_settings(self):
        self.log("Opening settings window.")
        SettingsWindow(self)

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Settings")
        self.geometry("350x400")
        self.resizable(False, False)
        self.configure(bg=self.parent.config['Theme'].get('background', 'white'))
        self.transient(parent)
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")
        ttk.Label(main_frame, text="UI Settings", font=("Helvetica", 14, "bold")).pack(pady=(0, 15))
        self.create_color_picker(main_frame, "Background", "background")
        self.create_color_picker(main_frame, "Tabs/Accent", "tab_background")
        self.create_color_picker(main_frame, "Button", "button_background")
        self.create_color_picker(main_frame, "Button Active", "button_active")
        self.create_color_picker(main_frame, "Button Text", "button_text")
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)
        ttk.Label(main_frame, text="User Settings", font=("Helvetica", 14, "bold")).pack(pady=(0, 15))
        ttk.Label(main_frame, text="Saved Roblox Cookie").pack(anchor="w", pady=(0, 2))
        self.cookie_entry = ttk.Entry(main_frame, show="*", width=40)
        self.cookie_entry.insert(0, self.parent.config.get('User', 'roblosecurity', fallback=''))
        self.cookie_entry.pack(fill="x", pady=(0, 20))
        save_button = ttk.Button(main_frame, text="Save and Apply", command=self.save_and_apply)
        save_button.pack(fill="x")

    def create_color_picker(self, parent, label_text, config_key):
        frame = ttk.Frame(parent)
        frame.pack(fill='x', pady=2)
        label = ttk.Label(frame, text=label_text)
        label.pack(side='left')
        color = self.parent.config['Theme'].get(config_key)
        color_box = tk.Label(frame, text="", bg=color, width=4, relief='sunken', borderwidth=1)
        color_box.pack(side='right')
        def choose_color():
            new_color = colorchooser.askcolor(color=color_box['bg'], title=f"Choose {label_text} Color")[1]
            if new_color:
                color_box.config(bg=new_color)
                self.parent.config.set('Theme', config_key, new_color)
        button = ttk.Button(frame, text="Choose", command=choose_color, style="Toolbutton")
        button.pack(side='right', padx=5)

    def save_and_apply(self):
        self.parent.config.set('User', 'roblosecurity', self.cookie_entry.get())
        self.parent.save_settings()
        self.parent.load_saved_cookie()
        messagebox.showinfo("Settings Saved", "Settings have been saved and applied.", parent=self)
        self.destroy()

if __name__ == "__main__":
    app = RobloxAssetDownloader()
    app.mainloop()
