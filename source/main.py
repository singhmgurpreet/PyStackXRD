import os
import pandas
from pandas.errors import ParserError
from scipy.signal import savgol_filter
import csv

class StackDiffraction:
	def __init__(self):
		"""The lines below are commented out as they are defunct in the 
			GUI implementation"""
		#self.path = path
		#self.files = self.GetFiles()
		#self.data = [["2theta",*self.files],self.GetThetaValues(),*self.GetHistograms()]

	def GetFiles(self,path,extension=".csv"):
		files = list(filter(lambda f: f.endswith(extension),
						os.listdir(path)))
		return sorted(files,key = lambda f: os.path.getctime(path+"/"+f))

	def GetThetaValues(self,path):
		rows_to_skip = 1
		read_file_successful = False
		while read_file_successful == False:
			try:
				df = pandas.read_csv(path+"/"+self.files[0], 
									 skiprows = rows_to_skip,
									 header=None)
				read_file_successful = True
			except ParserError:
				rows_to_skip += 1
		df.columns = df.iloc[0]
		df = df[1:]
		return df["x"].astype("float32").to_list()

	def GetHistograms(self, path, files, separation,
						bkg_subt=False,
						norm=False,
						smooth = False,
						separate=False):
		histogram_INT = []
		offset = 0
		for index,file in enumerate(files):
			print(f"{index}\t -- \t{file}")
			rows_to_skip = 1
			read_file_successful = False
			while read_file_successful == False:
				try:
					df = pandas.read_csv(path+"/"+file, 
										 skiprows = rows_to_skip,
										 header=None)
					read_file_successful = True
				except ParserError:
					rows_to_skip += 1
			df.columns = df.iloc[0]
			df = df[1:]
			if not(bkg_subt or norm or smooth or separate):
				histogram_INT.append((df["y_obs"].astype("float32").to_list()))
			else:
				df["y"] = df["y_obs"].astype("float32")
				if bkg_subt:
					df["y"] = (abs(df["y"] - df["y_bkg"].astype("float32")))
				if norm:
					df["y"] = (df["y"]/max(df["y"]))
				if smooth:
					df["y"] = (savgol_filter(df["y"],11,2))
				if separate:
					df["y"] = (df["y"] + offset)
					offset += separation
				histogram_INT.append((df["y"].to_list()))
			
		return histogram_INT

	def SaveCSV(self,filename):
		with open(filename,"w",newline="") as f:
			csvwriter = csv.writer(f,delimiter=",")
			csvwriter.writerow(self.data[0])
			csvwriter.writerows(list(zip(*self.data[1:])))

if __name__ == "__main__":
	"""The lines below are commented out as they they are defunct in the GUI implementation."""
	#testfunc = StackDiffraction("G:\\My Drive\\SBU\\PyStackXRD\\SampleDirectory")
	#testfunc.SaveCSV()