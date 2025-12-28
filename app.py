import streamlit as st
import requests

st.title("🔥 FLAMES Game")

# ---- Discord webhook (use secrets later) ----
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1454856516145250305/pFKHwwDmT3nqccrcZbjzFpGewVlpw1qKrskuocXO-QGrZ-mdNmXyh4HGXu1NJQyCGmXh"

# ---- Session flag to prevent repeat sending ----
if "discord_sent" not in st.session_state:
    st.session_state.discord_sent = False

name1 = st.text_input("Enter first name")
name2 = st.text_input("Enter second name")

if st.button("Get Result"):

    # reset flag on every new click
    st.session_state.discord_sent = False

    if not name1 or not name2:
        st.warning("Please enter both names")
    else:
        # FLAMES logic
        a = list(name1.lower())
        b = list(name2.lower())

        for i in a.copy():
            if i in b:
                a.remove(i)
                b.remove(i)

        n = len(a + b)
        s = "flames"

        while len(s) != 1:
            i = n % len(s) - 1
            if i == -1:
                s = s[:-1]
            else:
                s = s[i + 1:] + s[:i]

        d = {
            'f': 'Friends',
            'l': 'Love',
            'a': 'Affection',
            'm': 'Marriage',
            'e': 'Engaged',
            's': 'Siblings'
        }

        result = d[s]
        st.success(result)

        # ---- Send to Discord ONLY ONCE ----
        if not st.session_state.discord_sent:
            payload = {
                "content": (
                    f"🔥 **FLAMES Played**\n"
                    f"Name 1: **{name1}**\n"
                    f"Name 2: **{name2}**\n"
                    f"Result: **{result}**"
                )
            }

            requests.post(WEBHOOK_URL, json=payload)
            st.session_state.discord_sent = True
