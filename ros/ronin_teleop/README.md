- #### ronin_teleop

  Teleoperación remota del robot
  
  - **launch/**

    - *ps4_teleop_joy.launch*: lanza el nodo de teleoperación con la configuración del joystick de PS4
    
  - **param/**    
  
    - *mocute_bt.yaml*: configuración para joystick bluetooth mocute 
    - *ps4.yaml*: configuración para joystick PS4
    - *xbox.yaml*: configuración para joystick XBox
    
  - **scripts/**    
  
    - *ronin_teleop_joy.py*: nodo de gestión del joystick
