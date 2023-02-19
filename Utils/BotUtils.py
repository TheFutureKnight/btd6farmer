from pathlib import Path
import time
import re
import mss
try: # THIS IS SO UGLY BUT IT WORKS, I DONT WANNA BOTHER WITH PACKAGING AND STUFF
    from . import ocr, monitor, recognition, logger # If running from main.py
except ImportError:
    import ocr, monitor, recognition, logger # If running from this file

import concurrent.futures
log = logger.logger

class BotUtils:
    def __init__(self, DEBUG: bool = False):
        self.DEBUG = DEBUG
        self.round_area = None

    def getRoundArea(self):
        # Init round area dict with width and height of the round area
        round_area = {
            "width": 200,
            "height": 42
        }

        # Search for round text, returns (1484,13) on 1080p
        area = self.checkFor("round", return_cords=True, center_on_found=False) 
        log.debug("this should be only printed once, getting round area")
        log.debug(f"Round area found at {area}, applying offsetts")
        
        if area:
            log.info("Found round area!")

            # set round area to the found area + offset
            x, y, roundwidth, roundheight = area
            
            # Fiddled offset, do not tuch
            # Offset from ROUND text to round number
            xOffset = roundwidth + 10
            yOffset = int(roundheight * 3) - 40

            round_area["top"] = y + yOffset
            round_area["left"] = x - xOffset

            return round_area

        # If it cant find anything
        log.warning("Could not find round area, setting default values")
        default_round_area_scaled = monitor.scaling([0.7083333333333333, 0.0277777777777778]) # Use default values, (1360,30) on 1080p

        # left = x, top = y
        round_area["left"] = default_round_area_scaled[0]
        round_area["top"] = default_round_area_scaled[1]
        return round_area

    def getRound(self):
        # If round area is not located yet
        if self.round_area is None:
            self.round_area = self.getRoundArea()
        
        # Setting up screen capture area
        # The screen part to capture
        screenshot_dimensions = {
            'top': self.round_area["top"], 
            'left': self.round_area["left"], 
            'width': self.round_area["width"], 
            'height': self.round_area["height"] + 50
        }

        # Take Screenshot
        with mss.mss() as screenshotter:
            screenshot = screenshotter.grab(screenshot_dimensions)
            found_text, _ocrImage = ocr.getTextFromImage(screenshot)
            
            if self.DEBUG:
                from cv2 import imwrite, IMWRITE_PNG_COMPRESSION
                def get_valid_filename(s):
                    s = str(s).strip().replace(' ', '_')
                    return re.sub(r'(?u)[^-\w.]', '', s)
                imwrite(f"./DEBUG/OCR_DONE_FOUND_{get_valid_filename(found_text)}_{str(time.time())}.png", _ocrImage, [IMWRITE_PNG_COMPRESSION, 0])

            # Get only the first number/group so we don't need to replace anything in the string
            if re.search(r"(\d+/\d+)", found_text):
                found_text = re.search(r"(\d+)", found_text)
                return int(found_text.group(0))
            else:
                # If the found text does not match the regex requirements, Debug and save image
                log.warning("Found text '{}' does not match regex requirements".format(found_text))
                
                try:
                    file_path =  Path(__file__).resolve().parent.parent/ "DEBUG"
                    if not file_path.exists():
                        Path.mkdir(file_path)

                    with open(file_path/f"GETROUND_IMAGE_{str(time.time())}.png", "wb") as output_file:
                        output_file.write(mss.tools.to_png(screenshot.rgb, screenshot.size))
                    
                    log.warning("Saved screenshot of what was found")

                except Exception as e:
                    log.error(e)
                    log.warning("Could not save screenshot of what was found")

                return None
            

    def checkFor(self, 
            images: list[str] | str, 
            confidence: float = 0.9, 
            return_cords: bool = False, 
            center_on_found: bool = True,
            return_raw: bool = False
        ) -> bool:
        """Generic function to check for images on screen"""

        assets_directory = Path(__file__).resolve().parent/"assets"
        image_path = lambda image : assets_directory/f"{image}.png"
        if isinstance(images, list):
            
            output = [None]*len(images)
            
            # Could this be done the find function?
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Submit the template matching function to the thread pool
                futures= {
                    executor.submit(recognition.find, image_path(image)): idx for idx, image in enumerate(images)
                }
                
                # When all the tasks are done, return the results in the same order as the input
                for future in concurrent.futures.as_completed(futures):
                    output[futures[future]] = future.result()
            
            # Return the raw output if return_raw is true
            if return_raw:
                return output

            # Return true if any of the images are found
            return any(output)
        else:
            return recognition.find(
                image_path(images), 
                confidence, 
                return_cords, 
                center_on_found
            )
        

if __name__ == "__main__":
    bot = BotUtils(DEBUG=True)
    time.sleep(5)
    print(bot.getRound())