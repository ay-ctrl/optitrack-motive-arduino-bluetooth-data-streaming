import time
import serial

from natnet_client import DataDescriptions, DataFrame, NatNetClient

prev = time.time()

ser=serial.Serial('COM7',9600) # This COM7 number can be changed when you repower the arduino, it should be the same with com port number with your arduino
time.sleep(2)

def send_rigidbody_pos(data_frame:DataFrame):
    global prev
    current=time.time()
    rb=data_frame.rigid_bodies[0]
    if (current - prev)> 0.05:
        position=f"({rb.pos[0]:.6f},{rb.pos[1]:.6f},{rb.pos[2]:.6f})"
        print(str(position))
        position+="\n"
        ser.write(position.encode()) # sending rigidbody position information to arduino via serial port
        prev=current

num_frames = 0
if __name__ == "__main__":
    streaming_client = NatNetClient(server_ip_address="169.254.109.96", local_ip_address="169.254.109.96", use_multicast=False)
    streaming_client.on_data_frame_received_event.handlers.append(send_rigidbody_pos)
    with streaming_client:
        while True:
            streaming_client.update_sync()
            streaming_client.request_modeldef()
           
ser.close()        
