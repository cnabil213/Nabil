# lance une commande, affiche son temps et sa RAM pic (ru_maxrss de l'enfant) ; remplace /usr/bin/time -v absent de la machine
import subprocess, resource, time, sys, json
t = time.time(); r = subprocess.run(sys.argv[1:]); ru = resource.getrusage(resource.RUSAGE_CHILDREN)
print(json.dumps({"MESURE": {"elapsed_s": round(time.time() - t, 2), "ram_pic_mb": round(ru.ru_maxrss / 1024), "exit": r.returncode}}))
sys.exit(r.returncode)
