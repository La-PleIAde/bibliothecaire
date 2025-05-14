from bibliothecaire import CombinedDownloader, process_directory


def download_hugo(downloads_folder):
    downloader = CombinedDownloader(base_folder=downloads_folder)
    downloader.download_all("Victor Hugo")

def clean_hugo(downloads_folder):
    process_directory(downloads_folder + "/Victor_Hugo", downloads_folder + "/cleaned_Victor_Hugo")

def main():
    downloads_folder = "downloads"
    download_hugo(downloads_folder)
    clean_hugo(downloads_folder)

if __name__ == "__main__":
    main()
    print("Done!")
