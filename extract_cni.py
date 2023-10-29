#For this code, thanks to these tutorials https://www.geeksforgeeks.org/image-registration-using-opencv-python/ and https://pysource.com/2018/07/20/find-similarities-between-two-images-with-opencv-and-python/
# where the code and the steps are explained with comments
import time
import cv2
import numpy
def getSimilarity(kp_1, desc_1, template,orb,flann):
    kp_2, desc_2 = orb.detectAndCompute(template, None)
    matches = flann.knnMatch(desc_1, desc_2, k=2)
    
    good_points = []
    for m_n in matches:
        if len(m_n) != 2:
            continue
        (m,n) = m_n
        if m.distance < 0.6*n.distance:
            good_points.append(m)
    number_keypoints = min(len(kp_1), len(kp_2))
    #Not beautiful to return an array with a lot of things but it means you don't have to redo FLAAN's knnMatch and ORB's detectAndCompute so it optimizes the code
    return [len(good_points)/number_keypoints, good_points, [kp_1, kp_2]]

def isNew(image, orb, flann):
  start = int(round(time.time() * 1000))
  #We check the relatio between the good matches(Lowe's Ratio Test) and all the keypoints
  #To optimize the code, you can just put an "else" for old cards instead of double-checking if it's an old card.
  templatenew = cv2.imread("template-new-cni.jpg")
  kp_1, desc_1 = orb.detectAndCompute(image, None)
  similarity_new = getSimilarity(kp_1, desc_1, templatenew, orb,flann)
  print(similarity_new[0]*100)
  templateold = cv2.imread("template-old-cni.jpg")
  similarity_old = getSimilarity(kp_1, desc_1, templateold, orb,flann)
  print(similarity_old[0]*100)

  if(similarity_new[0]>3*similarity_old[0]):
        print("br")
        print("isNew runned during "+str(int(round(time.time() * 1000))-start))
        return [True, similarity_new]
  elif(similarity_old[0]>3*similarity_new[0]):
        print("isNew runned during "+str(int(round(time.time() * 1000))-start))
        return [False, similarity_old]
  else:
      return [None,None]
  
def getCNI(tobealigned):
    starttime = int(round(time.time() * 1000))
    reference = None
    orb_detector = cv2.ORB_create(6500)
    flann = cv2.FlannBasedMatcher(dict(algorithm = 6, table_number = 6,  key_size = 12,  multi_probe_level = 1), dict())
    isCNINew = isNew(tobealigned, orb_detector, flann)
    match(isCNINew[0]):
        case True:
            reference = cv2.imread("template-new-cni.jpg")
            print("new card")
        case False:
            reference = cv2.imread("template-old-cni.jpg")
            print("old card")
        case _:
            print("CARTE INVALIDE")
            exit()
    #We get all the informations returned by isNew()
    height, width = reference.shape[:2]
    kp1, kp2 = isCNINew[1][2]
    good_points = isCNINew[1][1]
    src_pts = numpy.float32([ kp1[m.queryIdx].pt for m in good_points]).reshape(-1,1,2)
    dst_pts = numpy.float32([ kp2[m.trainIdx].pt for m in good_points]).reshape(-1,1,2)
    homography = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)[0]
    transformed_img = cv2.warpPerspective(tobealigned, homography, (width, height))
    #Your CNI is straightened !
    print("The program runned during "+str(int(round(time.time() * 1000))-starttime))
    return [transformed_img, isCNINew[0]]
# If you want to test
# cv2.imshow("mat",getCNI(cv2.imread("test-old.jpg"))[0])
# cv2.waitKey(0)