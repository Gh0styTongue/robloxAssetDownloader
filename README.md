# Roblox Asset Downloader

You found it. The only Roblox asset downloader you'll ever need, now in a sleek Python package. While other tools struggle, this one just works.

This desktop application, built with Python, is for downloading any Roblox asset you throw at it. Yes, that includes the ones others can't handle.

-----

## Why Is This Different? 👑

Let's be clear: other asset downloaders fail when it comes to videos. They'll hand you a useless playlist file—basically a text document—and call it a day. They leave you stranded, trying to figure out how to piece together a video from a cryptic file that no media player understands. It's a broken, confusing experience.

This is the **first and only Roblox asset downloader** that actually understands how Roblox videos work.

When you give it a video asset ID, it doesn't just dump a useless file on you. It works its magic behind the scenes, automatically handling the complex streaming format, finding the highest quality version, and delivering the final, playable video file directly to your downloads folder. No manual work, no confusing steps, no extra software needed.

It just works. The way it was supposed to from the beginning.

-----

## Features

  * **Pioneering Video Downloader**: The only tool that automatically downloads Roblox's complex video streams.
  * **Individual & Bulk Downloading**: Download assets one by one or in large batches.
  * **Private Asset Support**: Effortlessly download private assets using your `.ROBLOSECURITY` cookie and a Place ID.
  * **Customizable UI**: Don't like the default look? Change the application's colors to fit your style.
  * **Secure Cookie Storage**: Safely save your `.ROBLOSECURITY` cookie so you don't have to enter it every time.
  * **Verbose Logging**: Every single action is logged to a timestamped file, because we believe in transparency.

-----

## Prerequisites

  * **Python 3.x**
  * **pip** (Python's package installer)
  * **requests** library

-----

## Installation

1.  **Get the code:**
    ```sh
    git clone https://github.com/Gh0styTongue/robloxAssetDownloader.git
    ```
2.  **Navigate into the directory:**
    ```sh
    cd robloxAssetDownloader
    ```
3.  **Install the single dependency:**
    ```sh
    pip install requests
    ```
4.  **Run it:**
    ```sh
    python blox.py 
    ```

-----

## Usage

It's straightforward:

1.  Launch the application.
2.  Fill in the fields:
      * **Roblox Cookie** (Optional): Your `.ROBLOSECURITY` cookie. You'll need it for private assets.
      * **Place ID** (Optional): The game's ID, also for private assets.
      * **Asset ID(s)**: The ID of the asset(s) you want. For bulk, put each ID on a new line.
3.  Click **Download**.
4.  Check your "Downloads" folder.

-----

## Settings

Click the "Settings" button to make the application yours.

  * **UI Settings**: Change the colors. Go wild.
  * **User Settings**: Save your `.ROBLOSECURITY` cookie in the local configuration file. It's loaded automatically on startup.

-----

## FAQ

  * **Is this against Roblox's ToS?**
      * No. It uses the official Roblox APIs as intended.
  * **Is it safe?**
      * Yes. Your cookie is stored locally and is only ever sent to official Roblox servers.
  * **What can I download?**
      * Everything. Models, decals, audio, and—unlike any other tool—videos.
## License

This project is licensed under the MIT License.
