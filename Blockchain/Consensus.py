class QConsensus:

    def validate(self, node_data):
        return True  # placeholder

    def commit(self, block):
        return {
            "status": "committed",
            "hash": hash(str(block))
        }
