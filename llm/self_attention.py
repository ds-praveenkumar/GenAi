
import torch
import  torch.nn as nn
torch.manual_seed(0)

class SelfAttention(nn.Module):
    def __init__(self, d_in, d_out) :
        super().__init__()
        self.d_in = d_in
        self.d_out = d_out
        self.Wq = nn.Linear(self.d_in, self.d_out, )
        self.Wk = nn.Linear(self.d_in, self.d_out, )
        self.Wv = nn.Linear( self.d_in, self.d_out , )
        self.softmax = nn.Softmax(dim=2)
        
    def forward(self, x):
        query = self.Wq(x)
        key = self.Wk(x)
        value = self.Wv(x)
        scores = torch.bmm(query, key.transpose(1,2)) / (self.d_out ** 0.5)
        attention = self.softmax(scores) 
        hidden_stats = torch.bmm( attention, value)
        return hidden_stats
    
if __name__ == '__main__':
    # input_text = 'He is a good boy, he must score high'
    # tokens = input_text.lower().split()
    # VOCAB = set(tokens)
    VOACAB_SIZE = 10 #len( VOCAB )
    # index2text = {k:v for k,v in enumerate(tokens)}
    # print(index2text)
    # text2index = {v:k for k,v in index2text.items()}
    # print(text2index)
    # embedding = [text2index[key] for key in tokens]
    # pad_list = []
    # pad_list = [-100 for x in range((VOACAB_SIZE - len(embedding)) +1)]
    # print(pad_list)
    # print( embedding+pad_list)
    # data = torch.tensor( embedding , dtype=torch.float).reshape(1,2,VOACAB_SIZE)
    # print(data )
    data = torch.randint(1,10,size=(1,1,10), dtype=torch.float)
    print(data )
    # data =  torch.tensor(embedding, dtype=torch.float)
    # print(data )
    sa = SelfAttention(data.shape[-1],VOACAB_SIZE+1)
    out = sa.forward(data)
    print(f'result:\n {out}' )