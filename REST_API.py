import json
from flask import Flask, request, jsonify

app = Flask(__name__)


# 1. Registering a student as a voter.
# a. It will be necessary for new students to be registered to vote.

@app.route('/voterRegister', methods=['GET','POST'])
def query_records():
    name = request.args.get('name')
    id = request.args.get('id')
    phone = request.args.get('phone')
    email = request.args.get('email')
    major = request.args.get('major')

    data = {
        'name' : name,
        'id' : id,
        'phone' : phone,
        'email' : email,
        'major' : major
    }
    with open('./tmp/data.txt', 'a') as f:
        f.write(json.dumps(data) + '\n')
    return jsonify({'status': '200 Ok'})

# 2. De-registering a student as a voter.
# a. A student may need to be de-registered once they leave campus.
@app.route('/deregister', methods=['GET', 'DELETE'])
def deregister():
    id = request.args.get('id')
    name = request.args.get('name')
    new_records = []
    records = []

    with open('./tmp/data.txt', 'r') as f:
        for line in f:
            data = json.loads(line)
            records.append(data)
            print(data)
    new_records = [r for r in records if r['id'] != id]
    with open('./tmp/data.txt', 'w') as f:
        for r in new_records:
            f.write(json.dumps(r)+'\n')
    return jsonify(new_records)  


# 3. Updating a registered voter’s information.
# a. A student’s year group, major or other information might change.
@app.route('/edit-voter', methods=['GET', 'PUT'])
def editVoter():
    name = request.args.get('name')
    id = request.args.get('id')
    phone = request.args.get('phone')
    email = request.args.get('email')
    major = request.args.get('major')
    records = []
    new_data = {
        'name' : name,
        'id' : id,
        'phone' : phone,
        'email' : email,
        'major' : major
        }
    with open('./tmp/data.txt', 'r') as f:
        for line in f:
            data = json.loads(line)
            if data['id'] == id:
                data = new_data
                records.append(data)
            else:
                records.append(data)

    with open('./tmp/data.txt', 'w') as f:
        for r in records:
            f.write(json.dumps(r)+'\n')
    return jsonify(records)  

# 4. Retrieving a registered voter.
@app.route('/voter-profile', methods=['GET'])
def voterProfile():
    id = request.args.get('id')
    data = []
    with open('./tmp/data.txt', 'r') as f:
        data = [json.loads(line) for line in f if line.strip() if json.loads(line)["id"] == id]
        
    return jsonify(data)









# 5. Creating an election.
@app.route('/create-election', methods=['GET', 'POST'])
def createElection():
    id = request.args.get('id')
    Election = request.args.get('Election')
    Year = request.args.get('Election')
    Post = request.args.get('Post')
    Candidate = request.args.get('Candidate')
    records = []
    new_data = {
        'Election' : Election,
        'id' :id,
        'Year' : Year,
        'Post' : Post,
        'votes' : 0
        }
    with open('./tmp/electionData.txt', 'a') as f:
        f.write(json.dumps(new_data) + '\n')
    return jsonify({'status': '200 Ok'})

# 6. Retrieving an election (with its details)
@app.route('/election-results', methods=['GET'])
def electionResults():
    id = request.args.get('id')
    data = []
    with open('./tmp/ElectionData.txt', 'r') as f:
        data = [json.loads(line) for line in f if line.strip() if json.loads(line)["id"] == id]
        
    return jsonify(data)

# 7. Deleting an election.
@app.route('/delete-election', methods=['GET', 'DELETE'])
def deleteElection():
    id = request.args.get('id')
    name = request.args.get('Election')
    new_records = []
    records = []

    with open('./tmp/electionData.txt', 'r') as f:
        for line in f:
            data = json.loads(line)
            records.append(data)
            print(data)
    new_records = [r for r in records if r['id'] != id]
    with open('./tmp/electionData.txt', 'w') as f:
        for r in new_records:
            f.write(json.dumps(r)+'\n')
    return jsonify(new_records)  


# 8. Voting in an election
@app.route('/vote', methods=['GET', 'PUT'])
def Vote():
    Candidate = request.args.get('Candidate')
    id = request.args.get('id')

    records = []

    with open('./tmp/electionData.txt', 'r') as f:
        for line in f:
            data = json.loads(line)
            if data['id'] == id:
                data['votes']= int(data['votes'])+1
                records.append(data)
            else:
                records.append(data)

    with open('./tmp/electionData.txt', 'w') as f:
        for r in records:
            f.write(json.dumps(r)+'\n')
    return jsonify(records)  

if __name__ == '__main__':
    app.debug = True
    app.run()

