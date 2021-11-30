import matplotlib.pyplot as plt
import os.path


class OutputCreator:
    def __init__(self, message_sender, input_file_name, show_or_no_show):
        self.show_plots = show_or_no_show
        self.output_path = "outputs/"

        # Setup output directories and file names
        self.createOutputDir()
        self.getOutputFileName(input_file_name)

        self.save_output_file_from_transmission(message_sender)
        self.create_transmission_metric_plots(message_sender, show_or_no_show)

    def createOutputDir(self):
        # Create new directory for outputs
        output_dir_exists = os.path.exists(self.output_path)
        if not output_dir_exists:
            os.makedirs(self.output_path)

    def getOutputFileName(self, input_file_name):
        if(input_file_name == "webcam"):
            self.output_filename = "webcam_image_"
            self.output_ext = ".png"
        else:
            # Create output file name
            self.output_filename = os.path.splitext(os.path.basename(input_file_name))[0]
            self.output_ext =  os.path.splitext(os.path.basename(input_file_name))[1]
        self.output_file_path = self.output_path + "recieved_" + self.output_filename + self.output_ext



    def extract_payload_from_bitstream(self, bitstream):
            return bitstream[2:-1]

    def save_output_file_from_transmission(self,  message_sender):
        # Recreate bitstream from recieved bytes
        bt = bytes()
        for i, recievedFrame in enumerate(message_sender.received_frames):
            bt = bt + self.extract_payload_from_bitstream(recievedFrame)

        print("Saving recieved file to: " + self.output_file_path)
        with open(self.output_file_path,'wb') as ofile:
            ofile.write(bt) 

    def create_transmission_metric_plots(self, message_sender, show_or_no_show):
        fig, axs = plt.subplots(2,figsize=(16,9))
        fig.suptitle('Transmission Metric Plots Over Time')
        plt.subplots_adjust(top=0.85)
        fig.tight_layout(pad=2, w_pad=5, h_pad=5)

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
        fig.savefig(self.output_path + "transmission_metrics_" + self.output_filename + '.png')
        if show_or_no_show:
            fig.show()
            a=input()