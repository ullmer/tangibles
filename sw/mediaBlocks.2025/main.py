# Original code by Brygg Ullmer, John Alex, et al., MIT Media Lab, 1998
# Port co-lead by CoPilot 2025
# Begun 2025-06-08

from sequencer.sequencer import Sequencer
from visualization.pivy_visualization import PivyVisualization
from communication.plasma_communication import PlasmaCommunication

def main():
    config_path = 'mediaBlocks/config/config.yaml'
    db_path = 'mediaBlocks/data/database.sqlite'

    sequencer = Sequencer(config_path, db_path)
    visualization = PivyVisualization(sequencer.config['visualization'])
    communication = PlasmaCommunication(sequencer.config['communication'])

    # Example usage
    sequencer.create_sequence('Example Sequence', 3, ['item1', 'item2', 'item3'])
    sequences = sequencer.get_sequences()
    print('Sequences:', sequences)

    for seq in sequences:
        items = sequencer.get_sequence_items(seq[0])
        print(f'Sequence {seq[1]} items:', items)

    visualization.setup()
    visualization.render()

    communication.connect()
    communication.send_message('Hello, Plasma!')
    message = communication.receive_message()
    print('Received message:', message)

if __name__ == '__main__':
    main()
