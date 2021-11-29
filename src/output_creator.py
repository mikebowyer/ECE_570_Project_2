import matplotlib.pyplot as plt

# Print Metrics!
def create_transmission_metric_plots(message_sender, show_or_no_show):
    plt.plot(message_sender.latencies, c="g", alpha=0.5)
    plt.xlabel("Index of frame sent")
    plt.ylabel("Latency in milliseconds")
    plt.title("Frame Transmission Latencies")
    plt.show()
    # plt.savefig('books_read.png')

    plt.plot(message_sender.success_rate, c="g", alpha=0.5)
    plt.xlabel("Index of frame sent")
    plt.ylabel("Packet Transmission Success Rate")
    plt.title("Packet Transmission Success Rate Over Time")
    plt.show()