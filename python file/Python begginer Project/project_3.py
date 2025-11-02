import os
def find_winner(bidders_details):
    # print(bidders_details)
    highest_bid=0
    winner=""
    for bidder in bidders_details:
        bidding_price=bidders_details[bidder]
        print(f'bidder :{bidder}')
        if bidding_price > highest_bid:
             highest_bid=bidding_price
             winner=bidder 
    print(f'here is all bidders detail {bidders_details}')
    print(f'the winner is {winner} in a bid of {highest_bid}')
bidders_data={}
end_bid=False
while not end_bid:
    
     name=input('Enter your name :')
     price=int(input('Enter a bid price :'))
     bidders_data[name]=price
     more_bidders=input('Is there any other bidder? type yes or no :').lower()
     if more_bidders=="no":
          end_bid=True
          find_winner(bidders_data)
     elif more_bidders == 'yes':
         os.system('cls')





