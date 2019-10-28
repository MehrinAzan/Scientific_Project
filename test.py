import numpy as np
import cv2
import matplotlib as plt


# Skin thickness
# automized ROI cropping
# mask lines on border


pic1 = imread('pic2_cropped.jpg');

pic1_gray = rgb2gray(pic1) #Convert to grayscale
[height, width] = size(pic1_gray) #Number of rows and columns


% loop to define height of ROI depending on height of image
if height < 0.4*width
    maxHeight = height*0.4;
else
    maxHeight = height*0.15;
end
maxHeight = fix(maxHeight);

I1 = pic1_gray(1:maxHeight, :); %ROI
Isharp = imsharpen(I1); %sharpen image

%increase contrast
edgeThreshold = 0.9;
amount = 0.4;
Isharp = localcontrast(Isharp, edgeThreshold, amount);

Ig = imgaussfilt(Isharp, 1); %gaussian filtering
Ibin = im2bw(Ig, 110/255); %convert to binary

%-----------------------
% rectangular mask for edges
% to ensure that any holes on the edge are detected as holes

[rowsM, columnsM] = size(Ibin);
lineMask = zeros(rowsM, columnsM);

linHorSE = strel('rectangle', [1, columnsM]);  % horizontal line for top
linHor = linHorSE.Neighborhood;

linVer1SE = strel('rectangle',[rowsM, 1]);     % vertical line for left egde
linVer1=linVer1SE.Neighborhood;

linVer2SE = strel('rectangle',[rowsM, 1]);     % vertical line for right edge
linVer2 = linVer2SE.Neighborhood;

lineMask(1, 1:columnsM) = linHor;   % horizontal white line at top
lineMask(1:rowsM, 1) = linVer1;         % vertical line edge
lineMask(1:rowsM, columnsM) = linVer2;  % vertical line edge

Ibw = Ibin + lineMask;  % add mask to binary image

%-------------------------

% clean image
Ibwclean = bwareaopen(Ibw, 400); %remove objects with fewer than 400 pixels
Ibwfill = imfill(Ibwclean, 'holes');


%loops to remove unnecessary objects for eventual sum of pixels
[row,column] = size(Ibwfill);
imgSkin = zeros(row, column); %empty matrix

for ccount=2:(column - 1) %column counter. exclude vertical mask lines
    for rcount=1:row %row counter
     if Ibwfill(rcount,ccount)== 0
         break;
     else
         imgSkin(rcount,ccount)=Ibwfill(rcount,ccount); % fill empty matrix with returned values
     end
    end
end

[row2, column2] = size(imgSkin);
sumColumn = sum(imgSkin, 1);
totTh = sum(sumColumn); % total thickness of skin in each column in pixels
averageTh = sum(totTh)/column2; %average thickness of skin in pixels
fprintf('The average skin thickness in pixels is %.3f \n', averageTh);



% ---------------
% display images in steps

figure(1);
subplot(6, 1, 1);
imshow(I1);
title('ROI');

subplot(6,1,2);
imshow(Isharp);
title('with Adjustments');

subplot(6,1,3);
imshow(Ig);
title('with Gaussian Filtering');


subplot(6,1,4);
imshow(Ibw);
% c = 2; r = 15; %starting points for boundary
% boundary = bwtraceboundary(Ibw, [r, c], 'N');
% imshow(Ibw)
% hold on;
% plot(boundary(:,2), boundary(:,1), 'r', 'LineWidth', 3) %display boundary
% hold off
title('Binarized');


subplot(6,1,5);
imshow(Ibwfill);
title('Cleaned image');


subplot(6,1,6);
imshow(imgSkin);
title('ROI - Skin Only');


