from speak import  LangParams, ListenLoop


lang_en = LangParams("en", "en-US",
                     phrases = ["Wark", "Vark listen to me",
                      "ukrainska", "ukrajinska", "ukraine",
                      "find box", "find the box", "find the bottle","find bottle"],
                     start_phrase = "I'm ready! Talk to me"
                     )

def df_action(action):
    print("Action from DF:"+action)

listen =  ListenLoop(rate=16000,
                     project_id="testproject-363201",
                     df_action = df_action,
                     lang = lang_en,
                     device=2
                     )

while(True):
    listen.run()
