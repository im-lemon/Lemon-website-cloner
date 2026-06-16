import urllib.parse
from multiprocessing.dummy import Pool
import requests, bs4, argparse, os, urllib
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="The website to clone.", required=True)
args = parser.parse_args()

os.makedirs("lemon-cloner_output/", exist_ok=True)
path = os.path.join("lemon-cloner_output/")
with open(f"{path}/hi.md", 'w') as hi:
    hi = hi.write("Hello, this file is here as a placeholder. " \
    "If there are no contents in the output directory except this file, there might not be any CSS/Images on/in the site you want to scrape. " \
    "It could also be caused by an internal error in the cloner, "
    "if so, please open an issue on our Github repository [here.](https://github.com/im-lemon/lemon-website-cloner)")


if not args.input.startswith("https://") and not args.input.startswith("http://"):
    args.input = "https://" + f"{args.input}"
req = requests.get(args.input)
time.sleep(0.1)
if req.status_code >= 400:
    print("Something went wrong with the request;", req.text)
    sys.exit()

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

                end_url = urllib.parse.urljoin(args.input, src).split("?")[0]
                time.sleep(0.1)
                req_img = requests.get(end_url)
                fn = os.path.basename(end_url)
                fn = fn.replace(" ", "_")
                fn = fn.replace("+", "_")
                f_path = os.path.join("lemon-cloner_output/", "images/", fn)
                with open(f"{f_path}", "wb") as f:
                    f.write(req_img.content)
                    print(fn)
        print("Successfully fetched all images..")

    
    # Get ALL CSS from site.

    css_files = soup.find_all("link", rel="stylesheet")
    if not css_files:
        print("No CSS Files found! ):")
    else:
        os.makedirs("lemon-cloner_output/CSS", exist_ok=True)
        with Pool(100) as pool:
            for css_file in pool.imap_unordered(lambda i: i, css_files):
                css_src = css_file["href"]

                css_end_url = urllib.parse.urljoin(args.input, css_src).split("?")[0]
                css_fn = os.path.basename(css_end_url)
                req_css = requests.get(css_end_url)
                time.sleep(0.1)

                css_f_path = os.path.join("lemon-cloner_output/", "CSS/", css_fn)
                with open(css_f_path, 'w', encoding='utf-8') as f:
                    f.write(req_css.text)
                    print(css_fn) #type:ignore
            print("Done fetching CSS...")
    
#   Get all HTML
    if not req.text:
        print("No HTML files found! ):")
    else:
        os.makedirs("lemon-cloner_output/HTML", exist_ok=True)

    # rewrite all paths to point to our fetched files.

    for img in imgs:
        imgog = img["src"]
        this_img_fn = os.path.basename(imgog) #type:ignore
        if "?" in this_img_fn:
            c = this_img_fn.find("?")
            clean = this_img_fn[:c]
        else:
            clean = this_img_fn
        clean = urllib.parse.unquote(clean)
        clean = clean.replace(" ", "_")
        clean = clean.replace("+", "_")
        img["src"] = f"../Images/{clean}"
        print("Cleaned Image...")

    for cssrc in css_files:
        cssog = cssrc["href"]

        this_css_fn = os.path.basename(cssog) #type:ignore

        if "?" in this_css_fn:
            c = this_css_fn.find("?")
            clean = this_css_fn[:c]
        else:
            clean = this_css_fn
        cssrc["href"] = f"../CSS/{clean}"

        txt=soup.prettify()
        with open("lemon-cloner_output/HTML/index.html", 'w', encoding='utf-8') as f:
            f.write(txt)
    print("Saved HTML file locally.")