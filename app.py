import base64
import io
import random
from flask import Flask, Response, jsonify, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from uncertainty import load_prof_data, chose_best_question,plot, compute_posterior,parse_yes_no,is_certain,compute_uncertainty
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend

import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


app = Flask(__name__, template_folder="templates")
def plunk(prof_pmf):
    plt.rcParams['font.family'] = 'Comic Sans MS'
    plt.rcParams['axes.facecolor'] = '#27445D'
    plt.rcParams['figure.facecolor'] = '#27445D'

    COLOR = 'white'
    plt.rcParams['text.color'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rc('axes', edgecolor=COLOR)
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR

    # Create figure and axis
    fig, ax = plt.subplots()
    ax.bar(prof_pmf.keys(), prof_pmf.values(), color='white')
    ax.set_xticklabels(prof_pmf.keys(), rotation=90, fontsize=5)
    ax.set_xlabel("Prof Names")
    ax.set_ylabel("Probabilities")
    ax.set_title("Probability of your culprit")

    # Attach the Agg backend to the figure (this is the correct way!)
    canvas = FigureCanvas(fig)

    # Save plot to an in-memory buffer
    img = io.BytesIO()
    canvas.print_png(img)  # Render figure to PNG
    plt.close(fig)  # Free memory

    return img.getvalue()  # Return PNG image as binary data

###
prof_pmf, question_data = load_prof_data('professors.csv')
    #print(prof_pmf)
    #while not is_certain(prof_pmf):
  #  while not is_certain(prof_pmf):
 #       print("--------------------------")
 #       print_probs(prof_pmf)
 # #      print(f"=> Uncertainty: {compute_uncertainty(prof_pmf):.2f}")
  #      best_question = chose_best_question(prof_pmf, question_data)
  #      answer = parse_yes_no(input(f"{best_question} "))
  #      prof_pmf = compute_posterior(prof_pmf, question_data[best_question], answer)
  #      plot(prof_pmf).show()
        
 #   print("====================================\n")
  #  print(f"=> Uncertainty: {compute_uncertainty(prof_pmf):.2f}")
  #  print(f"Your culprit is {max(prof_pmf, key=prof_pmf.get)}")
def start():
    global prof_pmf,question_data
    prof_pmf,question_data = load_prof_data('professors.csv')
@app.route("/")
def index(question = None, certain = False):
    global prof_pmf,question_data
    # from flask import render_template
    if question is None:
        start()
        q = chose_best_question(prof_pmf, question_data)
    return render_template("index.html", question=q)

@app.route("/guess")
def guess():
    global prof_pmf,question_data
    """ renders the plot on the fly.
    """
    question = request.args.get("question")
    answer = request.args.get("answer")
    prof_pmf = compute_posterior(prof_pmf, question_data[question], parse_yes_no(answer))
    img_base64 = base64.b64encode(plunk(prof_pmf)).decode('utf-8')
    img_data_url = f"data:image/png;base64,{img_base64}"
    name = "na"
    if(is_certain(prof_pmf)):
        name = max(prof_pmf, key=prof_pmf.get)
    data = {
        'img': img_data_url,
        'certain': is_certain(prof_pmf),
'uncertainty': f"=> Uncertainty: {compute_uncertainty(prof_pmf):.2f}",
        'name': name
    }
    return jsonify(data)
@app.route("/next")
def nextq():
    q = chose_best_question(prof_pmf, question_data)
    data = { 'question': q, 'uncertainty': f"Uncertainty: {compute_uncertainty(prof_pmf):.2f}"}
    return jsonify(data)

if __name__ == "__main__":
    import webbrowser
    port = int(os.environ.get('PORT', 6969))

    webbrowser.open("http://127.0.0.1:6969/")
    app.run(port=port, debug=True)
