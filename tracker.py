import math                   #imports the math module which provides mathematical functions
class Tracker:                #defines a class named "Tracker"
    def __init__(self):       #defines a constructor method that is called when an object of the "Tracker" class is created
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0


    def update(self, objects_rect):        #defines a method that takes the objects bounding boxes as input and updates the center points of the objects.
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:            #iterates over the bounding boxes of the objects
            x, y, w, h = rect                #unpacks the bounding box coordinates into four variables.
            cx = (x + x + w) // 2            #computes the x-coordinate of the center point of the object.
            cy = (y + y + h) // 2            #computes the y-coordinate of the center point of the object.

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():        # iterates over the center points of the previously detected objects.
                dist = math.hypot(cx - pt[0], cy - pt[1])    #computes the Euclidean distance between the center point of the current object and the center point of a previously detected object

                if dist < 35:                                #checks if the distance is less than a threshold value (35 in this case)
                    self.center_points[id] = (cx, cy)        #This line assigns the center coordinates (cx, cy) to an object with ID 
                    print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id]) #The entry consists of the bounding box coordinates (x, y, w, h) and the object ID id.
                    same_object_detected = True              #exit the inner loop if an object with similar center coordinates has already been detected in a previous frame.
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])    # The bounding box coordinates and the new object ID are added to the objects_bbs_ids list 
                self.id_count += 1                                     # The self.id_count variable is incremented to keep track of the next available object ID

# Clean the dictionary by center points to remove IDS not used anymore
#The loop iterates over each entry in objects_bbs_ids, extracts the object ID, looks up the center coordinates in the self.center_points dictionary, and assigns the center coordinates to the new_center_points dictionary
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids