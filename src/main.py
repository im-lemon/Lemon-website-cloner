from encodings.punycode import T
from fnmatch import fnmatch
import urllib.parse
from multiprocessing.dummy import Pool
import requests, bs4, argparse, os, urllib

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="The website to clone.", required=True)
args = parser.parse_args()

os.makedirs("lemon-cloner_output/", exist_ok=True)
path = os.path.join("lemon-cloner_output/")
with open(f"{path}/hi.md", 'w') as hi:
    hi = hi.write("Hello, this file is here as a placeholder. " \
    "If there are no contents in the output directory except this file, there might not be any CSS/Images on/in the site you want to scrape. " \
    "It could also be caused by an internal error in the cloner, "
    "if so, please open an issue on our Github repository [here](https://github.com/im-lemon/lemon-website-cloner)")


if not args.input.startswith("https://") and not args.input.startswith("http://"):
    args.input = "https://" + f"{args.input}"
req = requests.get(args.input)
if req.status_code != 200:
    print("Something went wrong with the request;", req.text)

else:

#   Get all images from site.
    
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    imgs = soup.find_all("img")
    if not imgs:
        print("No images found! ):")
    else:
        os.makedirs("lemon-cloner_output/images", exist_ok=True)
        with Pool(100) as pool:
            for image in pool.imap_unordered(lambda i: i, imgs):
                src = image["src"]

                end_url = urllib.parse.urljoin(args.input, src) #type:ignore
                req_img = requests.get(end_url)
                fn = os.path.basename(end_url)
                f_path = os.path.join("lemon-cloner_output/", "images/", fn)
                with open(f"{f_path}", "wb") as f:
                    f.write(req_img.content)
                    print(fn)
        print("Successfully fetched all images..")

    
    # Get ALL CSS from site.
    
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    css_files = soup.find_all("link", rel="stylesheet")
    if not css_files:
        print("No CSS Files found! ):")
    else:
        os.makedirs("lemon-cloner_output/CSS", exist_ok=True)
        with Pool(20) as pool:
            for css_file in pool.imap_unordered(lambda i: i, css_files):
                css_src = css_file["href"]

                css_end_url = urllib.parse.urljoin(args.input, css_src).split("?")[0]
                css_fn = os.path.basename(css_end_url)
                req_css = requests.get(css_end_url)

                css_f_path = os.path.join("lemon-cloner_output/", "CSS/", css_fn)
                with open(css_f_path, 'w', encoding='utf-8') as f:
                    f.write(req_css.text)
                    print(css_fn) #type:ignore
            print("Done fetching CSS...")