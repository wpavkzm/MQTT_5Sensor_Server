# Test_MQTT_Sercer
sensor MQTT server create


**apt and ilb set
**

1. sudo apt-get update
2. sudo apt-get install mosquitto
3. sudo apt-get install mosquitto-clients
4. sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
5. sudo apt clean
6. wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
7. sudo apt-key add mosquitto-repo.gpg.key
8. sudo reboot

**after reboot
**


**단축키 모음(실행)
**

1. mosquitto(서버실행)
2. sudo service mosquitto stop (누군가 내서버를 방해할때 서버 강제종료)
3. sudo service mosquitto start(강제종료 한 서버를 살릴때)
4. mosquitto_pub -h <localhost> -t <토픽주제선정> -m "보낼메세지"
  

**암호화 및 세팅 파일 설정 - 서버 데이터 해킹 방지 및 보안설정
**
  
sudo mosquitto_passwd -c /etc/mosquitto/passwd dave
Password:  <password>
rePassword: <password>
sudo nano /etc/mosquitto/conf.d/default.conf (실행이 안될때는 하위 디텍토리로 가서 실행)
allow_anonymous false
password_file /etc/mosquitto/passwd
(5,6번 추가)
sudo systemctl restart mosquitto
mosquitto_pub -t <토픽주제> -m <"메세지"> -P <"password">
