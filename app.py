import streamlit as st
import time
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Dragon Loader - Online Cash Game",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #ff6b35, #f7931e, #ffcc02);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .game-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .game-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 50px rgba(0,0,0,0.3);
    }
    
    .win-amount {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00ff00;
        text-shadow: 0 0 20px rgba(0,255,0,0.5);
        margin: 1rem 0;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(0,255,0,0.5); }
        to { text-shadow: 0 0 30px rgba(0,255,0,0.8); }
    }
    
    .play-cost {
        font-size: 1.4rem;
        color: #ffeb3b;
        font-weight: bold;
        background: rgba(255,235,59,0.1);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        display: inline-block;
    }
    
    .loading-container {
        text-align: center;
        padding: 4rem;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 20px;
        color: white;
        margin: 2rem 0;
    }
    
    .cashout-form {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border: 3px solid #28a745;
        box-shadow: 0 8px 32px rgba(40,167,69,0.2);
    }
    
    .balance-display {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .instant-badge {
        background: #dc3545;
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .stats-bar {
        background: linear-gradient(135deg, #ff9a56 0%, #ff6b35 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1.5rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'stage' not in st.session_state:
    st.session_state.stage = 'game_lobby'
if 'selected_game' not in st.session_state:
    st.session_state.selected_game = None
if 'game_details' not in st.session_state:
    st.session_state.game_details = {}
if 'loading_complete' not in st.session_state:
    st.session_state.loading_complete = False
if 'win_amount' not in st.session_state:
    st.session_state.win_amount = 0
if 'player_balance' not in st.session_state:
    st.session_state.player_balance = 0

# Game data
games_data = {
    "Golden Dragon Loader": {
        "icon": "🐲",
        "play_cost": "$5",
        "min_win": 10,
        "max_win": 500,
        "description": "Load the golden dragon and win instant cash! High-value spins with massive payout potential.",
        "win_rate": "78%",
        "avg_payout": "$45"
    },
    "Magic City Loader": {
        "icon": "🏰",
        "play_cost": "$3",
        "min_win": 5,
        "max_win": 250,
        "description": "Explore the magic city for instant rewards! Quick plays with consistent wins.",
        "win_rate": "82%",
        "avg_payout": "$28"
    },
    "Fire King Loader": {
        "icon": "🔥",
        "play_cost": "$10",
        "min_win": 20,
        "max_win": 1000,
        "description": "The ultimate high-stakes loader! Big risks, bigger rewards, instant cashouts.",
        "win_rate": "65%",
        "avg_payout": "$85"
    }
}

# Main header
st.markdown('<h1 class="main-header">🐉 DRAGON LOADER 🐉</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.3rem; color: #666; margin-bottom: 2rem;">💰 Play • Win • Cash Out Instantly • Real Money Games</p>', unsafe_allow_html=True)

# Stats bar
st.markdown("""
<div class="stats-bar">
    <h4>🔥 LIVE STATS</h4>
    <div style="display: flex; justify-content: space-around; margin-top: 1rem;">
        <div><strong>Players Online:</strong> 8,247</div>
        <div><strong>Total Paid Out Today:</strong> $127,583</div>
        <div><strong>Biggest Win:</strong> $2,450</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Game lobby
if st.session_state.stage == 'game_lobby':
    st.markdown("### 🎮 Choose Your Dragon Loader")
    
    for game_name, details in games_data.items():
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.markdown(f"""
            <div class="game-card">
                <h2>{details['icon']} {game_name}</h2>
                <p>{details['description']}</p>
                <div class="play-cost">{details['play_cost']} to Play</div>
                <div style="margin-top: 1rem;">
                    <span style="color: #00ff88;">💰 Win: ${details['min_win']}-${details['max_win']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Game Stats")
            st.metric("Win Rate", details['win_rate'])
            st.metric("Avg Payout", details['avg_payout'])
            
            # Win probability bar
            win_rate_num = int(details['win_rate'][:-1])
            st.write("**Win Probability**")
            st.progress(win_rate_num/100)
            
            st.markdown('<span class="instant-badge">⚡ INSTANT PAYOUT</span>', unsafe_allow_html=True)
        
        with col3:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button(f"🎮 Play {game_name.split()[0]}", key=f"play_{game_name}", use_container_width=True):
                st.session_state.selected_game = game_name
                st.session_state.game_details = details
                st.session_state.stage = 'loading'
                st.session_state.loading_complete = False
                st.rerun()

# Loading/Playing stage
elif st.session_state.stage == 'loading':
    st.markdown(f"### 🎮 Playing {st.session_state.selected_game}")
    
    st.markdown('<div class="loading-container">', unsafe_allow_html=True)
    
    if not st.session_state.loading_complete:
        st.markdown(f"### {st.session_state.game_details['icon']} Loading Dragon...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        loading_steps = [
            "🎰 Spinning the dragon wheel...",
            "💎 Calculating multipliers...",
            "🔥 Dragon magic activating...",
            "💰 Determining your payout...",
            "🎉 Game complete!"
        ]
        
        for i in range(101):
            progress_bar.progress(i)
            step_index = min(i // 20, len(loading_steps) - 1)
            status_text.markdown(f"### {loading_steps[step_index]}")
            time.sleep(0.03)
        
        # Determine if player wins (based on win rate)
        win_rate = int(st.session_state.game_details['win_rate'][:-1])
        if random.randint(1, 100) <= win_rate:
            # Player wins
            min_win = st.session_state.game_details['min_win']
            max_win = st.session_state.game_details['max_win']
            st.session_state.win_amount = random.randint(min_win, max_win)
            st.session_state.player_balance += st.session_state.win_amount
        else:
            # Player loses
            st.session_state.win_amount = 0
        
        st.session_state.loading_complete = True
        time.sleep(1)
        st.rerun()
    
    else:
        if st.session_state.win_amount > 0:
            st.success(f"🎉 WINNER! 🎉")
            st.markdown(f'<div class="win-amount">${st.session_state.win_amount}</div>', unsafe_allow_html=True)
            st.balloons()
        else:
            st.error("😔 Not a winner this time!")
            st.markdown('<div style="text-align: center; font-size: 1.5rem; color: #ff6b6b;">Better luck next spin!</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎮 Play Again", use_container_width=True):
                st.session_state.stage = 'game_lobby'
                st.session_state.loading_complete = False
                st.rerun()
        
        with col2:
            if st.session_state.player_balance > 0:
                if st.button(f"💰 Cash Out ${st.session_state.player_balance}", use_container_width=True):
                    st.session_state.stage = 'cashout'
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Cashout stage
elif st.session_state.stage == 'cashout':
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💰 Your Balance")
        st.markdown(f"""
        <div class="balance-display">
            <h2>💎 Available to Cash Out</h2>
            <div style="font-size: 3rem; font-weight: bold;">${st.session_state.player_balance}</div>
            <p>Ready for instant withdrawal!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### ⚡ Instant Payout Methods")
        st.write("💳 **Credit/Debit Card** - 2-5 minutes")
        st.write("📱 **PayPal** - Instant")
        st.write("💰 **Cash App** - Instant")
        st.write("🏦 **Bank Transfer** - 15-30 minutes")
    
    with col2:
        st.markdown("### 💸 Cash Out Form")
        st.markdown('<div class="cashout-form">', unsafe_allow_html=True)
        
        with st.form("cashout_form"):
            st.markdown(f"#### Withdrawing: ${st.session_state.player_balance}")
            
            # Personal info
            full_name = st.text_input("Full Name *", placeholder="Enter your full name")
            email = st.text_input("Email Address *", placeholder="Enter your email")
            phone = st.text_input("Phone Number *", placeholder="Enter your phone number")
            
            # Payout method
            st.markdown("#### Select Payout Method")
            payout_method = st.selectbox("Choose Method", 
                                       ["PayPal (Instant)", "Cash App (Instant)", 
                                        "Credit Card (2-5 min)", "Bank Transfer (15-30 min)"])
            
            if "PayPal" in payout_method:
                paypal_email = st.text_input("PayPal Email", placeholder="your@paypal.com")
            
            elif "Cash App" in payout_method:
                cashapp_tag = st.text_input("Cash App $Tag", placeholder="$YourCashTag")
            
            elif "Credit Card" in payout_method:
                card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
                card_name = st.text_input("Name on Card", placeholder="John Doe")
            
            elif "Bank Transfer" in payout_method:
                account_number = st.text_input("Account Number", placeholder="Account number")
                routing_number = st.text_input("Routing Number", placeholder="Routing number")
                bank_name = st.text_input("Bank Name", placeholder="Bank name")
            
            # Verification
            st.markdown("#### Identity Verification")
            id_type = st.selectbox("ID Type", ["Driver's License", "Passport", "State ID"])
            ssn_last4 = st.text_input("Last 4 digits of SSN", placeholder="1234", max_chars=4)
            
            # Terms
            terms_accepted = st.checkbox("I confirm all information is accurate and I am 18+ years old")
            
            submitted = st.form_submit_button("💰 Process Cash Out", use_container_width=True)
            
            if submitted:
                if not terms_accepted:
                    st.error("Please confirm your information and age.")
                elif not all([full_name, email, phone]):
                    st.error("Please fill in all required fields.")
                else:
                    # Process cashout
                    with st.spinner("Processing your cash out..."):
                        time.sleep(3)
                    
                    st.success(f"🎉 Cash out successful! ${st.session_state.player_balance} sent via {payout_method}")
                    st.balloons()
                    
                    # Reset balance
                    st.session_state.player_balance = 0
                    
                    if st.button("🎮 Play More Games", use_container_width=True):
                        st.session_state.stage = 'game_lobby'
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🐉 Dragon Loader | Real Money Gaming | Instant Payouts | 18+ Only</p>
    <p>📞 24/7 Support: 1-800-DRAGON | 💬 Live Chat Available | 🔒 SSL Secured</p>
    <p style="font-size: 0.8rem;">Licensed Gaming Platform • Responsible Gaming • Play Within Your Limits</p>
</div>
""", unsafe_allow_html=True)
