import matplotlib.pyplot as plt
import os.path

def extract_payload_from_bitstream(bitstream):
        return bitstream[2:-1]

def save_output_file_from_transmission(message_sender, input_file_name):
    # Create new directory for outputs
    output_path = "outputs/"
    output_dir_exists = os.path.exists(output_path)
    if not output_dir_exists:
        os.makedirs(output_path)
    
    # Recreate bitstream from recieved bytes
    bt = bytes()
    for i, recievedFrame in enumerate(message_sender.received_frames):
        bt = bt + extract_payload_from_bitstream(recievedFrame)

    # Create output file name
    base_file = os.path.basename(input_file_name)
    
    output_file_path = output_path + "recieved_" + base_file

    print("Saving recieved file to: " + output_file_path)
    with open(output_file_path,'wb') as ofile:
        ofile.write(bt) 


def create_transmission_metric_plots(message_sender, show_or_no_show):

    fig, axs = plt.subplots(2)
    fig.suptitle('Transmission Metric Plots Over Time')
    fig.tight_layout()

    # Plot Latency
    axs[0].plot(message_sender.latencies, c="g", alpha=0.5)
    axs[0].set(xlabel='Index of frame sent', ylabel='Latency in milliseconds', title='Frame Transmission Latencies')
    # axs[0].xlabel("Index of frame sent")
    # axs[0].ylabel("Latency in milliseconds")
    # axs[0].title("Frame Transmission Latencies")

    # Plot Transmission Success Rate
    axs[1].plot(message_sender.success_rate, c="g", alpha=0.5)
    axs[1].set(xlabel='Index of frame sent', ylabel='Packet Transmission Success Rate', title='Packet Transmission Success Rate Over Time')
    # axs[1].xlabel("Index of frame sent")
    # axs[1].ylabel("Packet Transmission Success Rate")
    # axs[1].title("Packet Transmission Success Rate Over Time")

    # Show and Save Fig
    fig.savefig('transmission_metrics.png')
    if show_or_no_show:
        fig.show()
        a=input()