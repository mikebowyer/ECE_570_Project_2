import matplotlib.pyplot as plt

# Print Metrics!
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