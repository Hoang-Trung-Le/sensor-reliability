%% Dempster-Shafer evidence theory for the Reliability of Air Quality Sensor

%% Section 1 Title
clc;
% Test run

featureMatrixH = [313.5     559.6   378.6   557.4   152.9   762.7;...
    1850.7    550.8   1734.5  597.21  152.3   808.2;...
    2669.3    546.6   2567.4  534.8   152.7   724.1];

samplingMatrixS = [1830.6   553.9   1780.5  600.2   152.5   1780.3;...
    2683.5   549.9   2502.4  590.0   151.9   1813.6;...
    2754.0   551.7   2638.1  595.4   152.1   1797.5;...
    2682.2   555.2   2557.3  575.5   152.5   1802.4];

probabilityMatrix = probMatrix(distMatrix(samplingMatrixS,featureMatrixH))
entropyShannon = entShannon(probabilityMatrix)
discountFactor = discFactor(entropyShannon)
discountedBPA = multiplyDiscountFactor(discountFactor,probabilityMatrix)
finalMassFunction = samplingsCombinedMassFunction(discountedBPA)

%%
clc

key = 'D80F3AFD-DDAD-11ED-BD21-42010A800008';
% Query parameters for the desired fields
params = struct();
params.group_id = '1872';
params.fields = 'name,latitude,longitude,humidity,temperature,pm2.5,pm10';
url = ['https://api.purpleair.com/v1/groups/', params.group_id, '/members'];

% Fetch JSON data from the API
response = webread(url, 'group_id',1872,'fields',params.fields, weboptions("KeyName",'X-API-Key','KeyValue',key));

%%
clear claases

pe = pyenv;
ObsRequest.StartDate = datetime('2023-07-23',"Format",'uuuu-MM-dd');
ObsRequest.EndDate = datetime('2023-07-25',"Format",'uuuu-MM-dd');
startDate = string(ObsRequest.StartDate);
endDate = string(ObsRequest.EndDate);
parameters = py.list({'HUMID','TEMP','PM2.5','PM10'});  % Create Python list
output = py.test10.getData(parameters, '107'); % (parameter, site_id, start_date, end_date)
data = jsondecode(string(output.text));

%%
clear
clc
import matlab.net.http.*
import matlab.net.http.field.*
% Query parameters for the desired fields
% headers = struct('content-type', 'application/json', 'accept', 'application/json');
urlAPI = 'https://data.airquality.nsw.gov.au/api/Data';
getSite = 'get_SiteDetails';
getParams = 'get_ParameterDetails';
getObs = 'get_Observations';
url = fullfile(urlAPI,getObs);
ObsRequest = struct();
ObsRequest.Parameters = "PM10";
ObsRequest.Sites = 107; % Liverpool: 107
ObsRequest.StartDate = datetime('2023-07-06',"Format",'uuuu-MM-dd');
ObsRequest.EndDate = datetime('2023-07-07',"Format",'uuuu-MM-dd');
ObsRequest.Categories = {'Averages'};
ObsRequest.SubCategories = {'Hourly'};
ObsRequest.Frequency = {'Hourly average'};

% payload = struct('Parameters', {''}, 'Sites', 107, 'StartDate', '2023-06-06', 'EndDate', '2023-06-07', 'Categories', {'Averages'}, 'SubCategories', {'Hourly'}, 'Frequency', {'24h rolling average derived from 1h average'});
data = ['key','=','value','&','Parameters','=', 'PM10'];
payload = struct('Parameters', "PM2.5", 'Sites', '107');

% Convert the payload to JSON string
% payloadStr = jsonencode(payload);
payload = '{ \"Parameters\": [ \"PM10\" ], \"Sites\": [ \"107\" ], \"StartDate\": \"2023-06-07\", \"EndDate\": \"2023-06-08\", \"Categories\": [ \"Averages\" ], \"SubCategories\": [ \"Hourly\" ], \"Frequency\": [ \"Hourly average\" ]}"';
% payload = '{ "Parameters": [ "PM10" ], "Sites": [ 107 ], "StartDate": "2023-06-07", "EndDate": "2023-06-08", "Categories": [ "Averages" ], "SubCategories": [ "Hourly" ], "Frequency": [ "Hourly average" ]}"';
payloadStr = jsonencode(payload);
delim = '&';
pairDelim = '=';
data = 107;
data = num2str(data);
data = ['key', pairDelim, 'value', delim, 'Sites', pairDelim, data];
% ObRequest = struct('Parameters', 'PM10', 'Sites', 107, 'StartDate', '2023-06-07', 'EndDate', '2023-06-08', 'Categories', 'Averages', 'SubCategories', 'Hourly', 'Frequency', 'Hourly average')
% payload = struct();
% payload.Parameters = {'PM10'};
% payload.Sites = [107];
% payload.StartDate = '2023-06-07';
% payload.EndDate = '2023-06-08';
% payload.Categories = {'Averages'};
% payload.SubCategories = {'Hourly'};
% payload.Frequency = {'Hourly average'};

% Convert payload to JSON string
% jsonPayload = jsonencode(payload);

% Create the HTTP request
body = matlab.net.http.MessageBody(payload);

% Convert payload to JSON string
jsonPayload = jsonencode(payload);
contentTypeField = matlab.net.http.field.ContentTypeField('application/json');
header = contentTypeField;
request = RequestMessage('POST', header, payload);
request.Body.Payload = payload;
show(request);
rep = send(request,url)
% Call the API using webread
% response = webread(url,"Parameters", {'PM2.5'}, 'Site_Id', '107',weboptions('HeaderFields',{'content-type' 'application/json'},'RequestMethod','post'));
response = webwrite(url,payload,weboptions('HeaderFields',{'content-type' 'application/json'},'RequestMethod','post','MediaType','application/x-www-form-urlencoded'));
% 'HeaderFields',{'Content-Type' 'application/json'; 'accept' 'application/json'},
%  'Parameters', 'PM10', 'Sites', 107, 'StartDate', '2023-06-07', 'EndDate', '2023-06-08', 'Categories', 'Averages', 'SubCategories', 'Hourly', 'Frequency', 'Hourly average'



%% Calculate combined mass
% For more than one sampling
function result = samplingsCombinedMassFunction(samplingsBPA)
    numSamplings = size(samplingsBPA,1);
    numHypos = size(samplingsBPA,3);
    DS = zeros(numSamplings, numHypos);
    for i = 1 : numSamplings
        DS(i,:) = combinedMassFunction(reshape(samplingsBPA(i,:,:),size(samplingsBPA,2),numHypos));
    end
    result = combinedMassFunction(DS);
end

% For more than one pair of evidence
% Input massFunc: (#features)-by-(#hypotheses)
% Output result: 1-by-(#hypotheses)
function result = combinedMassFunction(massFunc)
    numHypos = size(massFunc,2);
    interSteps = size(massFunc,1) - 1;
    stepMassFunction = zeros(size(massFunc));
    stepMassFunction(1,:) = massFunc(1,:);
    interMassFunc = zeros(numHypos, numHypos, interSteps);
    K = zeros(1,interSteps);
    for j = 1 : interSteps
        % Calculate the intermediate combined mass function of a pair of consecutive pieces of evidence

        % Calculation of intermediate mass function
        % Square matrix with size equals to number of hypotheses
        for i = 1 : numHypos
            interMassFunc(:,i,j) = stepMassFunction(j,i) * massFunc(j+1,:);
        end

        % Calculate the conflict coefficient
        d = diag(interMassFunc(:,1:(numHypos-1),j));
        K(j) = sum(interMassFunc(1:end-1, 1:end-1,j),"all") - sum(d,"all");

        % Calculation of combined intermediate mass function
        for i = 1 : (numHypos-1)
            stepMassFunction(j+1,i) = (interMassFunc(i,i,j)+interMassFunc(i,numHypos,j)+interMassFunc(numHypos,i,j))/(1-K(j));
        end
        stepMassFunction(j+1,numHypos) = interMassFunc(numHypos,numHypos,j)/(1-K(j));
    end
    result = stepMassFunction(end,:);
end

%%
function massFunction = calculateMassFunction(probMatrix, discountFactor)
    % Calculate the mass function from the probability matrix and discount factor

    % Multiply the probability matrix by the discount factor
    combinedMatrix = discountFactor .* probMatrix

    % Normalize the combined matrix along the third dimension
    normalizationFactor = sum(combinedMatrix, 3);
    normalizedMatrix = combinedMatrix ./ normalizationFactor;

    % Sum the rows along the third dimension to obtain the mass function
    massFunction = sum(normalizedMatrix, 2);

    % Normalize the mass function across all hypotheses
    massFunction = massFunction ./ sum(massFunction, 'all');
end

%% Shannon entropy
function sumEntropy = entShannon(probabilities)
    entropy = probabilities .* log(probabilities);
    % entropy(probabilities == 0) = 0;
    sumEntropy = -sum(entropy,3);
end

%% Discount factor
function DF = discFactor(ent)
    varEnt = var(ent(:),0);
    DF = 1 - (ent./(ent+varEnt));
end

%% Basic probability assignment
function resultMatrix = multiplyDiscountFactor(discountMatrix, probMatrix)
    % Multiply the discount factor matrix with all elements in the third dimension of the probability matrix

    % Get the size of the probability matrix
    [~, ~, numFeatures] = size(probMatrix);

    % Expand the discount factor matrix to match the size of the probability matrix
    expandedDiscountMatrix = repmat(discountMatrix, [1, 1, numFeatures]);

    % Multiply the discount factor matrix with the probability matrix element-wise
    resultMatrix = probMatrix .* expandedDiscountMatrix;
    resultMatrix(:, :, end+1) = 1 - sum(resultMatrix,3)
end


%% Distance matrix
function D = distMatrix(sampMat, featMat)
    D = zeros(size(sampMat,1), size(sampMat,2), size(featMat,1));
    for i = 1:size(featMat,1)
        D(:,:,i) = abs(sampMat - featMat(i,:));
    end
end

function normalisedP = probMatrix(distMatrix)
    P = 1 ./ distMatrix;
    normalisedP = P ./ sum(P, 3);
end


