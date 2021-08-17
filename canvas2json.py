import argparse
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
import base64
import ast


def main():
    parser = argparse.ArgumentParser(description="Scrape the <canvas> element from a URL to JSON")
    parser.add_argument("url", help="txt file name that contains URLs to be scrape")
    parser.add_argument("output", default="result", nargs='?', help="Path to the output folder, e.g. result/")
    parser.add_argument("save_png", default=1, nargs='?', choices=["0", "1"], help="whether to save png")
    args = parser.parse_args()

    # Input
    url_file = args.url
    with open(os.path.join(os.getcwd(), url_file)) as f:
        urls = f.readlines()

    # Output
    output_dir = os.path.join(os.getcwd(), args.output)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Save png or not
    save_png = args.save_png
    if int(save_png) == 1:
        save_png = True
    else:
        save_png = False
    
    # Config driver
    driver_path = "D:\\selenium_driver\\geckodriver"
    assert len(driver_path) > 0, "Please specify the browser driver path"
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path = driver_path, options=options)

    print("In total, there are %s url(s) to scrape" % len(urls))

    for url in urls: 
        
        # Remove line breaker in the txt file
        url = url.rstrip()
        url_name = re.sub('[\W_]+', '', url)

        try: 
            driver.get(url)
            # driver.get("http://curran.github.io/HTML5Examples/canvas/smileyFace.html")
            # driver.get("https://stats.warbrokers.io/players/i/5d2ead35d142affb05757778")
        except Exception:
            print("Cannot reach %s" % url)
            continue
        
        print("Now scraping %s" % url)

        canvases = driver.find_elements_by_tag_name("canvas")

        for idx, canvas in enumerate(canvases): 

            # get the canvas as a PNG base64 string
            # https://stackoverflow.com/questions/44806870/saving-canvas-to-json-and-loading-json-to-canvas
            canvas_str = driver.execute_script(
                '''
                var canvasContents = arguments[0].toDataURL();
                var data = { image: canvasContents, date: Date.now() };
                return JSON.stringify(data);
                ''', 
                canvas)

            # save to a file
            with open(os.path.join(output_dir, "%s_%s.json" % (url_name, idx)), 'w') as f:
                f.write(canvas_str)

            if save_png:
                
                # Convert dictionary-like string to dictionary
                di = ast.literal_eval(canvas_str)
                # Hard code to get the image string, then read it as bytes
                # https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
                s = str.encode(di["image"].split(",")[1])

                with open(os.path.join(output_dir, "%s_%s.png" % (url_name, idx)), "wb") as fh:
                    fh.write(base64.decodebytes(s))

    driver.quit()



if __name__ == "__main__":
    main()