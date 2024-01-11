import os
from PIL import Image
# 운석이미지 불러오기
rockImage = []
image_extesions = ['.png']
folder_path = "rock"
for filename in os.listdir(folder_path):
    file_extension = os.path.splitext(filename)[1].lower()  # 확장자를 추출하고 그 확장자를 소문자로 변환
    if file_extension in image_extesions:
        if filename.startswith("rock"):  # rock로 시작하는 파일 선별
            rockImage.append(os.path.join(folder_path, filename))  # 리스트에 넣음
            
print(rockImage)

#이미지 리사이즈
new_width = 20
new_height = 20

for filename in rockImage:
    image_path = os.path.join(folder_path, filename)
    
    try:
        #이미지 열기
        img = Image.open(image_path)
        
        #리사이즈
        img = img.resize((new_width, new_height))
        
        #리사이즈된 이미지 저장
        resized_image_path = os.path.join(folder_path,f"resized_{filename}")
        img.save(resized_image_path)
        
        print(f"{filename} 이미지를 리사이즈 하여 {new_width}x{new_height} 크기로 저장했습니다.")
    except Exception as e:
        print(f"{filename} 이미지를 처리하는 동안 오류 발생: {str(e)}")
            
