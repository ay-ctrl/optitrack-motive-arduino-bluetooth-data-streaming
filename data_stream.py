import time
import serial

from natnet_client import DataDescriptions, DataFrame, NatNetClient

prev = time.time()

ser=serial.Serial('COM7',9600) # This COM7 number can be changed when you repower the arduino, it should be the same with com port number with your arduino
time.sleep(2)

def recieve_unlabeled_marker_frame(data_frame:DataFrame): # this writes unlabeled marker data continuosly
    markers=data_frame.unlabeled_markers_pos  
    for marker in markers:
        print(f"Marker: X={marker[0]:.2f}, Y={marker[1]:.2f}, Z={marker[2]:.2f}")

def measure_time(): # to measure the time between two frame, you can call it in receive frame functions
    global prev
    current=time.time()
    if prev is not None:
        delta= current-prev
        print("Frame arası süre: ", delta)
    prev=current

def receive_labeled_marker_frame(data_frame: DataFrame): #this writes labeled marker data continously and send them to the serial port once in a second
    print("Labeled Rigid Bodies: ")
    for rb in data_frame.rigid_bodies:
        global prev
        current=time.time()
        if current-prev >=1.0:
            print(f"Rigid body id: {rb.id_num}")
            print(f"Position: X={rb.pos[0]:.2f}, Y={rb.pos[1]:.2f}, Z={rb.pos[2]:.2f}")
            print(f"Rotation: {rb.rot}")
            print("Markers (Rigid Body): \n")
            bdata=f"Rigid body id: {rb.id_num}\n"
            ser.write(bdata.encode())
            for i, marker in enumerate(rb.markers):
                data=f"Marker {i}: X={marker.pos[0]:.2f}, Y={marker.pos[1]:.2f}, Z={marker.pos[2]:.2f}\n"
                print(data)
                ser.write(data.encode())
            print("-")
            prev=current
            
def receive_and_send_data(data_frame:DataFrame): # this function directly sends required data to serial port without printing like receive_labeled_marker_frame function and in an easiable processable format
    global prev
    current=time.time()
    if current-prev >=1.0: # this time limit is for testing, for real time streaming, you can use send_real_time_data function
        db=(str)data_frame
        data="("
        for rb in data_frame.rigid_bodies:
            idn=rb.id_num
            rot=f"({rb.rot[0]:.2f},{rb.rot[1]:.2f},{rb.rot[2]:.2f})"
            pos=f"({rb.pos[0]:.2f},{rb.pos[1]:.2f},{rb.pos[2]:.2f})"
            marks="["
            for i, marker in enumerate(rb.markers):
                mar=f"({i},{marker.pos[0]:.2f},{marker.pos[1]:.2f},{marker.pos[2]:.2f})"
                marks+=mar
            marks+="]"
            data+=f"[{idn},{rot},{pos},{marks}],"
        data+=")\n"
        ser.write(db.encode()) # sending required rigidbody information in a tuple ( [rb_id, (rot), (pos), [(marker1 pos), (marker2 pos),....]], [other rb_id, (rot), (pos), [(marker1 pos), (marker2 pos),....]] )
            
        prev=current

def send_real_time_data(data_frame:DataFrame):
    data="("
    for rb in data_frame.rigid_bodies:
        idn=rb.id_num
        rot=f"({rb.rot[0]:.2f},{rb.rot[1]:.2f},{rb.rot[2]:.2f})"
        pos=f"({rb.pos[0]:.2f},{rb.pos[1]:.2f},{rb.pos[2]:.2f})"
        marks="["
        for i, marker in enumerate(rb.markers):
            mar=f"({i},{marker.pos[0]:.2f},{marker.pos[1]:.2f},{marker.pos[2]:.2f})"
            marks+=mar
        marks+="]"
        data+=f"[{idn},{rot},{pos},{marks}],"
    data+=")\n"
    ser.write(data.encode()) # sending required rigidbody information in a tuple ( [rb_id, (rot), (pos), [(marker1 pos), (marker2 pos),....]], [other rb_id, (rot), (pos), [(marker1 pos), (marker2 pos),....]] )

def receive_new_desc(desc: DataDescriptions): # this will be called when new data descriptions are defined (for example when you create a new rigid body in motive)
    print("Received data descriptions.")
    #print(desc)

num_frames = 0
if __name__ == "__main__":
    streaming_client = NatNetClient(server_ip_address="169.254.109.96", local_ip_address="169.254.109.96", use_multicast=False)
    streaming_client.on_data_description_received_event.handlers.append(receive_new_desc)
    #streaming_client.on_data_frame_received_event.handlers.append(receive_labeled_marker_frame) # to print and send labeled marker data, this can be more time consuming
    #streaming_client.on_data_frame_received_event.handlers.append(send_real_time_data)
    streaming_client.on_data_frame_received_event.handlers.append(receive_and_send_data)

    with streaming_client:
        while True:
            streaming_client.update_sync()
            streaming_client.request_modeldef()
           
ser.close()        
