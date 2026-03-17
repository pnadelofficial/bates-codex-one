import json
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

BASE_URL = "/bates-codex-one"
CONTENT_FILE = Path("content/items.json")
TEMPLATES_DIR = Path("templates")
STATIC_DIR = Path("static")
OUTPUT_DIR = Path("output")

def load_items() -> list[dict]:
    with open(CONTENT_FILE) as f:
        return json.load(f)
    
def setup_jinja() -> Environment:
    return Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=True,
    )
 
def copy_static():
    dest = OUTPUT_DIR / "static"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(STATIC_DIR, dest)
    print(f"  Copied static assets → {dest}")

def build_index(env: Environment, items: list[dict]):
    template = env.get_template("index.html")
    html = template.render(items=items, active_page="home", base_url=BASE_URL)
    out = OUTPUT_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"  Built {out}")

def build_browse(env: Environment, items: list[dict]):
    template = env.get_template("browse.html")
    html = template.render(items=items, active_page="browse", base_url=BASE_URL)
    out = OUTPUT_DIR / "browse.html"
    out.write_text(html, encoding="utf-8")
    print(f"  Built {out}")
 
def build_item_pages(env: Environment, items: list[dict]):
    template = env.get_template("item.html")
    out_dir = OUTPUT_DIR / "items"
    out_dir.mkdir(parents=True, exist_ok=True)
 
    for i, item in enumerate(items):
        html = template.render(
            item=item,
            prev_item=items[i - 1] if i > 0 else None,
            next_item=items[i + 1] if i < len(items) - 1 else None,
            active_page="browse",
            base_url=BASE_URL,
        )
        out = out_dir / f"{item['id']}.html"
        out.write_text(html, encoding="utf-8")
 
    print(f"  Built {len(items)} item pages → {out_dir}")

# def build_about(env: Environment):
#     template = env.get_template("about.html")
#     html = template.render(active_page="about", base_url=BASE_URL)
#     out = OUTPUT_DIR / "about.html"
#     out.write_text(html, encoding="utf-8")
#     print(f"  Built {out}")

if __name__ == "__main__":
    print("Building site...")
 
    OUTPUT_DIR.mkdir(exist_ok=True)
 
    items = load_items()
    env = setup_jinja()
 
    copy_static()
    build_index(env, items)
    build_browse(env, items)
    build_item_pages(env, items)
    # build_about(env)
 
    print(f"\nDone. {len(items)} items built → {OUTPUT_DIR}/")