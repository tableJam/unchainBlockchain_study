class Candidate:
    def __init__(self, candidate_id, name):
        self.id = candidate_id
        self.name = name
        self.vote_count = 0


class ElectionApp:
    def __init__(self):
        self.voters = {}  # Stores whether an address has voted
        self.candidates = {}  # Stores candidate info by candidate ID
        self.candidates_count = 0
        
    def add_candidate(self, name):
        self.candidates_count += 1
        self.candidates[self.candidates_count] = Candidate(self.candidates_count, name)
        
    def vote(self, voter_address, candidate_id):
        # Check if voter has already voted
        if self.voters.get(voter_address):
            raise Exception("You have already voted.")
        
        # Check if candidate ID is valid
        if candidate_id <= 0 or candidate_id > self.candidates_count:
            raise Exception("No candidate with the given ID")
        
        # Record that voter has voted
        self.voters[voter_address] = True
        
        # Update candidate vote count
        self.candidates[candidate_id].vote_count += 1
        
        # In Solidity, an event would be emitted. In Python, we might print a message or handle this some other way.
        print(f'Voted event: {candidate_id}')


## ethereum
##　「スマートコントラクトをデプロイする」というのは、ブロックチェーン上にクラスのインスタンスを作ることを意味します。
## bitcoinはブロックチェーン技術で、合意可能な「数値データ」の単一の状態を作りました。ethereumは、合意可能な「インスタンス」の単一の状態を作ります。ここが重要！
###########################
election = ElectionApp() ## deploy contract
##########################in blockchain


## change state
##send transaction about add candidate
election.add_candidate("Alice")#<----- transaction送信(状態変更)
election.add_candidate("Bob")#<------ transaction送信(状態変更)　つまり、インスタンスの状態変数を変更する、ethereumの場合は。。。。。。


## transaction for vote!!!
election.vote("0x123", 1)# <------------transaction送信(状態変更)