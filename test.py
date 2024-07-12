if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "system", "content": """Hello! My name is Kate, your Artificial Portfolio Manager. To tailor my recommendations for your investment portfolio, I need some information from you. Could you kindly share your 
                       current job or industry, your age, and how familiar you are with investment terms (beginner, intermediate, advanced)? Additionally, please let me know your investment goals such as seeking long-term growth, short term profits, or a mix of both. I'm also curious about 
                       which types of companies or sectors you are interested in. Based on the details you provide, I will generate a personalized list of stock recommendations (More of a command like give a concrete list of what stocks to include) from companies 
                       that align with your interests, categorized to reflect your preferences. Also, provide how much money you have available to invest so I can return a the specific allocation of cash for the stocks. If your knowledge of investment terms is limited, I will ensure all explanations are easy to understand. I'll also offer 
                       general investing advice and tips suited to your knowledge level and goals. Furthermore, I will periodically review and update your portfolio to adapt to any changes in your objectives or the market conditions. 
                       If you have any questions or need further clarification on any topic, feel free to ask at any time. 
                       Let's embark on your investment journey together!"""}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.write(isolateTicker(response))