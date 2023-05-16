from ultralytics import YOLO
import cv2
import numpy as np
import yaml
import math

# Open config.yaml File
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

frame_size = 640*640 # image input size

# Object detection function, input is image & model
def segment(file, model ,latitude, zoomLevel):
    ponds_dict = {}
    
    image=file
    
    
    # Inference YOLOv8
    result = model.predict(
        source=image, # image input
        conf=cfg["yolov8"]["conf"], # confidence threshold
        device='cpu') # device (defualt 0 (gpu), change to "cpu" to use cpu)
    
    # Plot detection result image
    img_yolo = result[0].plot()
    print("imgYOLO", img_yolo.shape)
    # Retrive result information
    prob = result[0].boxes.cls
    problist = prob.tolist() # change type from tensor to list
    countListDetected = [len(problist)] # count total detected for each class

    # Retrive boundingbox information
    boxes = result[0].boxes.xywh # get list xywh for each detected object
    boxes_list = boxes.tolist() # change type from tensor to list

    masks = (result[0].masks.xy)
    count = int(len(masks))

    METERS_PER_PX = (156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoomLevel))
    RATIO_PIXEL_TO_SQUARE_M = METERS_PER_PX*METERS_PER_PX
    n=1
    for i in range(len(result)):
        for j in range(len(result[i].masks)):
            segmenPoly = result[i].masks[j].xy
            
            x1 = int(result[i].boxes[j].xyxy[0][0])
            y1 = int(result[i].boxes[j].xyxy[0][1])
            x2 = int(result[i].boxes[j].xyxy[0][2])
            y2 = int(result[i].boxes[j].xyxy[0][3])

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            for x in segmenPoly:
                for y in x:
                    y[0] = round(y[0])
                    y[1] = round(y[1])

            pts = np.array(segmenPoly[0], np.int32)
            pts = pts.reshape((-1, 1, 2))

            img = cv2.polylines(image, [pts], True, (255, 0, 0), 2)
            img = cv2.putText(img, f"{n}", (center_x, center_y), cv2.FONT_HERSHEY_PLAIN, 3 , (255,255,255), 5)
            areaPX = cv2.contourArea(pts) * RATIO_PIXEL_TO_SQUARE_M

            ponds_dict[n] = areaPX
            n+=1
    
    return ponds_dict, countListDetected, img_yolo



