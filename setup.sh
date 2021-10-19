mkdir -p ~/.streamlit/

echo "\
[theme]\
primaryColor='#F63366'\
backgroundColor='#FFFFFF'\
secondaryBackgroundColor='#F0F2F6'\
textColor='#262730'\
font='sans serif'\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
