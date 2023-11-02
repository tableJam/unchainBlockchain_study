import time
import json
import hashlib
DIFFICULTY = 3;
SENDER = 'SATOSHINAKAMOTO';
REWORD = '0.1';

def sort_by_key(target:dict):
    sorted_dict = {}
    for key in sorted(target.keys()):
        sorted_dict[key] = target[key]
    return sorted_dict


class Blockchain():
  ##ここでは、簡易的にBitcoinNodeを再現します。
  def __init__(self,minerAddress:str):
    self.chain = [];
    self.transactionPool = [];
    self.createBlock(0,self.hash({}));
    self.minerAddress = minerAddress;

  def createBlock(self,nonce:int,previousHash:str):
    block = sort_by_key({
      'timestamp': time.time(),
      'transactions': self.transactionPool,
      'nonce': nonce,
      'previous_hash':previousHash
    });
    self.chain.append(block);
    self.transactionPool = [];

  def hash(self,block:dict):
    sortedBlock = json.dumps(block,sort_keys=True);
    return hashlib.sha256(sortedBlock.encode()).hexdigest();

  def addTransaction(self,senderAddress:str,recipientAddress:str,value:int):
    transaction = sort_by_key({
      'sender_address': senderAddress,
      'recipient_address': recipientAddress,
      'value': value
    });
    self.transactionPool.append(transaction);
    # if len(self.transactionPool) >= 4:
    #   self.mining();

  def proofOfWork(self):
    transactions = self.transactionPool.copy();
    previousHash = self.hash(self.chain[-1]);
    nonce = 0;
    while self.work(transactions,previousHash,nonce)==False:
      nonce+=1;
    return nonce;

  def work(self,transaction:list, previousHash:str,nonce:int,difficulty=DIFFICULTY):
    guessBlock = sort_by_key({
      'transactions': transaction,
      'nonce': nonce,
      'previous_hash': previousHash
    })
    guessHash = self.hash(guessBlock);
    return guessHash[:difficulty] == '0'*difficulty;

  def mining(self):
    self.addTransaction(SENDER,self.minerAddress,REWORD);
    previousHash = self.chain[-1];
    nonce = self.proofOfWork();
    self.createBlock(nonce,previousHash);


  def balanceOf(self,targetAddress:str):
    balance = 0;
    for block in self.chain:
      for tx in block['transactions']:
        value = tx['value'];
        if tx['recipient_address'] == targetAddress:
          balance += value;
        elif tx['sender_address'] == targetAddress:
          balance -= value;
    return balance;


# トランザクションが送信され、一定数がtransactionPoolに溜まると、それがブロックに詰められ、コンセンサスアルゴリズム(proof of work)を介して、検証され、チェーンに追加されます。・

if __name__ == '__main__':
  
  blockchain = Blockchain('0x86939381938329');#instance of blockchainNode
  
  print('💰 lets start bitcoin ')
  
  blockchain.addTransaction('Alice','Bob',10); #alice がbobに10btc送りました。tx1
  blockchain.addTransaction('Tom','Alice',20); #Tomがaliceに20btc送りました。 tx2
  blockchain.addTransaction('Bob','Tom',30); #BobがTomに30btc送りました。 tx3
  blockchain.addTransaction('Alice','Bob',40); #alice がbobに40btc送りました。tx4
  blockchain.mining();# ここで、マイニングが実行され、tx1,2,3,4がブロックに詰められ,Blockの信憑性が検証され、チェーンに追加されます。
  bobBtc =  blockchain.balanceOf('Bob')#bobの残高を確認します。
  
  for block in blockchain.chain:
    for tx in block['transactions']:
      print(tx);
      
  print('bob has',bobBtc, 'btc');


# bitcoinは、中央集権的な機関を擁せず、分散型のシステムによって、信頼性のある取引を実現しています。
# ここで重要なことは、bitcoinはその革新的なシステム(ブロックチェーンと呼ばれるようになる)によって、合意可能な唯一無二の状態を実現しているということです。
# ブロックチェーン技術は、情報を、分散的に、透明性高く、保持できることによって、合意可能な唯一無二の状態を実現することができます。