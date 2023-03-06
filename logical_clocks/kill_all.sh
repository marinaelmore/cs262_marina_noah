#kill all processes that have the name "python"
ps | grep "python app.py --machine_id" | awk '{print $1}' | xargs kill -9