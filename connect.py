import subprocess

def run_node_command(donation_amount):
    node_command = 'node C:\\Users\\aashi\\OneDrive\\Desktop\\MHack\\Backend\\src\\index.js ' + str(donation_amount) + ' "0.0.5906653"'
    print(node_command)
    process = subprocess.run(node_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode != 0:
        print("Error:", process.stderr.decode('utf-8'))
    else:
        result = process.stdout.decode('utf-8')
        print(result)