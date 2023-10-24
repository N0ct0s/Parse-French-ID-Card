#For this code, thanks to these tutorials https://www.geeksforgeeks.org/image-registration-using-opencv-python/ and https://pysource.com/2018/07/20/find-similarities-between-two-images-with-opencv-and-python/
# where the code and the steps are explained with comments
import time
import cv2 
import numpy as np
def getSimilarity(kp_1, desc_1, template,sift):
    kp_2, desc_2 = sift.detectAndCompute(template, None)
    index_params = dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(desc_1, desc_2, k=2)
    good_points = []
    ratio = 0.6
    for m, n in matches:
        if m.distance < ratio*n.distance:
            good_points.append(m)
    #   result = cv2.drawMatches(image, kp_1, templatenew, kp_2, good_points, None)
    number_keypoints = 0
    if len(kp_1) <= len(kp_2):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)
    #   print("Keypoints 1ST Image: " + str(len(kp_1)))
    #   print("Keypoints 2ND Image: " + str(len(kp_2)))
    #   print("GOOD Matches:", len(good_points))
    #   print("How good it's the match: ", len(good_points) / number_keypoints * 100, "%")
    return len(good_points)/number_keypoints
def isNew(image):
  templatenew = cv2.imread("template-new-cni.jpg")
  sift = cv2.SIFT_create()
  kp_1, desc_1 = sift.detectAndCompute(image, None)

  if(getSimilarity(kp_1, desc_1, templatenew, sift) * 100 > 1.1):
     return True
  templateold = cv2.imread("template-old-cni.jpg")
  if (getSimilarity(kp_1, desc_1, templateold, sift)*100) > 1.1:
      return False
  else:
      return None
def getCNI(tobealigned):
    starttime = int(round(time.time() * 1000))
    reference = None
    isCNINew = isNew(tobealigned)
    match(isCNINew):
        case True:
            reference = cv2.imread("template-new-cni.jpg")
            print("new card")
        case False:
            reference = cv2.imread("template-old-cni.jpg")
            print("old card")
        case _:
            print("CARTE INVALIDE")
            exit()
    img1 = cv2.cvtColor(tobealigned, cv2.COLOR_BGR2GRAY) 
    img2 = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY) 
    height, width = img2.shape 
    orb_detector = cv2.ORB_create(5000) 
    kp1, d1 = orb_detector.detectAndCompute(img1, None) 
    kp2, d2 = orb_detector.detectAndCompute(img2, None) 
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) 
    matches = matcher.match(d1, d2)  
    matches=sorted(matches,key = lambda x: x.distance)
    matches = matches[:int(len(matches)*0.9)] 
    no_of_matches = len(matches) 
    p1 = np.zeros((no_of_matches, 2)) 
    p2 = np.zeros((no_of_matches, 2)) 
    for i in range(len(matches)): 
        p1[i, :] = kp1[matches[i].queryIdx].pt 
        p2[i, :] = kp2[matches[i].trainIdx].pt 
    homography = cv2.findHomography(p1, p2, cv2.RANSAC)[0]
    transformed_img = cv2.warpPerspective(tobealigned, homography, (width, height))
    print("The program runned during "+str(int(round(time.time() * 1000))-starttime))
    return transformed_img
# cv2.imshow("mat",getCNI(cv2.imread("test-new.jpg")))
# cv2.waitKey(0)