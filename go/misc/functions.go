package main

import (
	"image/png"
	"os"

	"golang.org/x/image/bmp"
)

func main() {
	err := convertBmpToPng("/home/bmaupin/Desktop/goldhill.bmp", "/home/bmaupin/Desktop/test.png")
	if err != nil {
		panic(err)
	}
}

func convertBmpToPng(inputBmpPath string, outputPngPath string) error {
	inputBmpFile, err := os.Open(inputBmpPath)
	if err != nil {
		return err
	}

	decodedImage, err := bmp.Decode(inputBmpFile)
	if err != nil {
		return err
	}

	outputPngFile, err := os.Create(outputPngPath)
	if err != nil {
		return err
	}

	err = png.Encode(outputPngFile, decodedImage)
	if err != nil {
		return err
	}

	return nil
}
